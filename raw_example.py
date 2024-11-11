import asyncio
import dataclasses
import io
import json
import logging
import os
import sys
import traceback
from asyncio.streams import FlowControlMixin, StreamReader, StreamWriter
from dataclasses import dataclass, field
from typing import Union

import aioconsole

LOG_FILENAME = "debug.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


@dataclass
class JsonRPCAction:
    id: int
    method: str
    parameters: field(default_factory=list)


@dataclass
class Result:
    title: str
    subtitle: str = ""
    icoPath: str = ""
    titleHighlightData: tuple[int] = ()
    titleTooltip: str = ""
    subtitleTooltip: str = ""
    copyText: str = ""
    jsonRPCAction: JsonRPCAction | None = None


@dataclass
class JsonRPCError:
    code: int
    message: str
    data: object = None


class JsonRPCException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


@dataclass
class JsonRPCQueryResponse:
    result: list[Result] = field(default_factory=list)
    settingsChanges: dict[str, object] = field(default_factory=dict)
    debugMessage: str = ""


@dataclass
class JsonRPCRequest:
    method: str
    id: int
    params: list[object] | None = None
    jsonrpc: str = "2.0"


@dataclass
class JsonRPCResult:
    id: int
    result: dict
    jsonrpc: str = "2.0"


@dataclass
class JsonRPCExecuteResponse:
    hide: bool = True


def write_line_to(file, msg):
    with open(file, "+a") as f:
        f.write(msg + "\n")


def clear_file(file):
    with open(file, "w"):
        pass


def encode_error(id: int, error: JsonRPCError):
    return (
        json.dumps(
            {
                "jsonrpc": "2.0",
                "error": dataclasses.asdict(error),
                "id": id,
            }
        )
        + "\r\n"
    ).encode("utf-8")


def encode_result(id: int, response: JsonRPCQueryResponse):
    return (
        json.dumps(
            {
                "jsonrpc": "2.0",
                "result": dataclasses.asdict(response),
                "id": id,
            }
        )
        + "\r\n"
    ).encode("utf-8")


class Client:
    def __init__(self) -> None:
        self.tasks: dict[int, asyncio.Task] = {}
        self.requests: dict[int, asyncio.Future[JsonRPCResult | JsonRPCError]] = {}
        self.request_id = 1

    async def __handle_cancellation(self, id: int):
        with open("cancel.log", "+a") as f:
            if id in self.tasks:
                f.write(f"cancel {id}, success: {self.tasks.pop(id).cancel()}\n")
            else:
                f.write(f"try cancel but no {id}\n")

    async def request(
        self, method: str, params: list[object] = []
    ) -> JsonRPCResult | JsonRPCError:
        waiter: asyncio.Future[JsonRPCResult | JsonRPCError] = asyncio.Future()
        self.request_id += 1
        self.requests[self.request_id] = waiter
        message = (
            json.dumps(
                dataclasses.asdict(JsonRPCRequest(method, self.request_id, params))
            )
            + "\r\n"
        )
        self.writer.write(message.encode("utf-8"))
        return await waiter

    async def __handle_result(self, result: JsonRPCResult):
        resultlogger.debug(f"result: {result.id}")
        if result.id in self.requests:
            self.requests.pop(result.id).set_result(result)
            return
        pass

    async def __handle_error(self, id: int, error: JsonRPCError):
        if id in self.requests:
            self.requests.pop(id).set_exception(Exception(error))
        else:
            errlogger.error(f"cancel with no id found: %d", id)

    async def __handle_notification(self, method: str, params: list[object]):
        if method == "$/cancelRequest":
            await self.__handle_cancellation(params["id"])
            return
        pass

    async def __handle_request(self, request: dict[str, object]):
        with open("debug.log", "+a") as f:
            f.write(f"{request}\n")
        method = request["method"]
        params = request["params"]
        try:
            task = asyncio.create_task(getattr(self, method)(*params))
            self.tasks[request["id"]] = task
            response = encode_result(request["id"], await task)
            debuglogger.debug("response %s", response.decode("utf-8"))
            self.writer.write(response)
            await self.writer.drain()
            return
        except json.JSONDecodeError:
            err = JsonRPCError(code=-32700, message="JSON decode error")
        except AttributeError:
            errlogger.exception()
            err = JsonRPCError(
                code=-32601, message="Method not found", data=f"{sys.exc_info()}"
            )
        except TypeError:
            errlogger.exception()
            err = JsonRPCError(code=-32602, message="Invalid params")
        except Exception:
            errlogger.exception()
            err = JsonRPCError(
                code=-32603, message="Internal error", data=f"{sys.exc_info()}"
            )
        self.writer.write(encode_error(request["id"], err))
        await self.writer.drain()

    async def start_listening(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer
        while True:
            bytes = await reader.readline()
            line = bytes.decode("utf-8")
            if line == "":
                continue
            querylogger.info(line)
            message = json.loads(line)
            if "id" not in message:
                asyncio.create_task(
                    self.__handle_notification(message["method"], message["params"])
                )
            elif "method" in message:
                asyncio.create_task(self.__handle_request(message))
            elif "result" in message:
                asyncio.create_task(self.__handle_result(JsonRPCResult(**message)))
            elif "error" in message:
                asyncio.create_task(
                    self.__handle_error(message["id"], JsonRPCError(**message["error"]))
                )


class Plugin(Client):
    async def initialize(self, arg: dict[str, object]):
        resultlogger.info(f"initialize: {json.dumps(arg)}")
        return JsonRPCExecuteResponse(hide=False)

    async def store(self, res):
        resultlogger.info(f"store: {json.dumps(res)}")
        return JsonRPCExecuteResponse(hide=False)

    async def query(self, arg: dict[str, object], settings: dict[str, object]):
        with open("test.log", "a+") as f:
            f.write(json.dumps(arg))
        result = await self.request("FuzzySearch", [arg["search"], "hello"])
        assert isinstance(result, JsonRPCResult)
        debuglogger.debug(result)
        res = JsonRPCQueryResponse(
            [
                Result(
                    f"hello: {result.result['score']}",
                    titleHighlightData=result.result.get("matchData", list()),
                    jsonRPCAction=JsonRPCAction(
                        id=0, method="store", parameters=[result.result]
                    ),
                )
            ]
        )
        return res


async def main():
    # loop = asyncio.get_event_loop()
    # reader = asyncio.StreamReader()
    # protocol = asyncio.StreamReaderProtocol(reader)
    # await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    # w_transport, w_protocol = await loop.connect_write_pipe(FlowControlMixin, sys.stdout)
    # writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)
    reader, writer = await aioconsole.get_standard_streams()
    client = Plugin()
    await client.start_listening(reader, writer)


if __name__ == "__main__":
    clear_file("cancel.log")
    clear_file("debug.log")
    clear_file("query.log")
    clear_file("test.log")
    clear_file("err.log")
    querylogger = setup_logger("querylogger", "query.log", level=logging.DEBUG)
    cancellogger = setup_logger("cancellogger", "cancel.log", level=logging.DEBUG)
    debuglogger = setup_logger("debuglogger", "debug.log", level=logging.DEBUG)
    errlogger = setup_logger("errlogger", "err.log", level=logging.ERROR)
    resultlogger = setup_logger("resultlogger", "result.log", level=logging.DEBUG)
    asyncio.run(main())
