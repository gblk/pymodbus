#!/usr/bin/env python3
"""Pymodbus aynchronous client example.

An example of a asynchronous client.

usage: client_async.py [-h] [--comm {tcp,udp,serial,tls}]
                       [--framer {ascii,binary,rtu,socket,tls}]
                       [--log {critical,error,warning,info,debug}]
                       [--port PORT]
options:
  -h, --help            show this help message and exit
  --comm {tcp,udp,serial,tls}
                        "serial", "tcp", "udp" or "tls"
  --framer {ascii,binary,rtu,socket,tls}
                        "ascii", "binary", "rtu", "socket" or "tls"
  --log {critical,error,warning,info,debug}
                        "critical", "error", "warning", "info" or "debug"
  --port PORT           the port to use
  --baudrate BAUDRATE   the baud rate to use for the serial device

The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import asyncio
import logging

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from examples import helper
from pymodbus.client import (
    AsyncModbusSerialClient,
    AsyncModbusTcpClient,
    AsyncModbusTlsClient,
    AsyncModbusUdpClient,
)


_logger = logging.getLogger()
_logger.setLevel("DEBUG")


def setup_async_client(description=None, cmdline=None):
    """Run client setup."""
    args = helper.get_commandline(
        server=False, description=description, cmdline=cmdline
    )
    _logger.info("### Create client object")
    if args.comm == "tcp":
        client = AsyncModbusTcpClient(
            args.host,
            port=args.port,  # on which port
            # Common optional paramers:
            framer=args.framer,
            #    timeout=10,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,
            #    strict=True,
            # TCP setup parameters
            #    source_address=("localhost", 0),
        )
    elif args.comm == "udp":
        client = AsyncModbusUdpClient(
            args.host,
            port=args.port,
            # Common optional paramers:
            framer=args.framer,
            #    timeout=10,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,
            #    strict=True,
            # UDP setup parameters
            #    source_address=None,
        )
    elif args.comm == "serial":
        client = AsyncModbusSerialClient(
            args.port,
            # Common optional paramers:
            #    framer=ModbusRtuFramer,
            #    timeout=10,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,
            #    strict=True,
            # Serial setup parameters
            baudrate=args.baudrate,
            #    bytesize=8,
            #    parity="N",
            #    stopbits=1,
            #    handle_local_echo=False,
        )
    elif args.comm == "tls":
        client = AsyncModbusTlsClient(
            args.host,
            port=args.port,
            # Common optional paramers:
            framer=args.framer,
            #    timeout=10,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,
            #    strict=True,
            # TLS setup parameters
            #    sslctx=sslctx,
            certfile=helper.get_certificate("crt"),
            keyfile=helper.get_certificate("key"),
            #    password="none",
            server_hostname="localhost",
        )
    return client


async def run_async_client(client, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    await client.connect()
    assert client.connected
    if modbus_calls:
        await modbus_calls(client)
    client.close()
    _logger.info("### End of Program")


async def run_a_few_calls(client):
    """Test connection works."""
    rr = await client.read_coils(32, 1, slave=1)
    assert len(rr.bits) == 8
    rr = await client.read_holding_registers(4, 2, slave=1)
    assert rr.registers[0] == 17
    assert rr.registers[1] == 17


if __name__ == "__main__":
    testclient = setup_async_client(description="Run asynchronous client.")
    asyncio.run(run_async_client(testclient, modbus_calls=run_a_few_calls), debug=True)
