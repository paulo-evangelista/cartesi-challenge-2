from os import environ
import logging
import requests
import marshal
import types
import traceback
import json
import dis

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ.get(
    "ROLLUP_HTTP_SERVER_URL", "http://localhost:8080/rollup")
logger.info(f"HTTP rollup server URL is {rollup_server}")

code = (
    b'\xe3\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00'
    b'\x00\x02\x00\x00\x00C\x00\x00\x00sR\x00\x00\x00d\x01}\x02d\x02}\x03'
    b'|\x02|\x03k\x03r\x19|\x02|\x03k\x04r\x11|\x02|\x038\x00}\x02n\x04'
    b'|\x03|\x028\x00}\x03|\x02|\x03k\x03s\x08|\x02|\x00k\x02r#|\x01d\x03'
    b'k\x02r#d\x04S\x00t\x00d\x05\x83\x01\x01\x00d\x06S\x00)\x07N\xe9\xff'
    b'\xff\x00\x00i\xe9\x01\x00\x00\xe99\x06\x00\x00T\xfa?Error calculating'
    b' GCD of a = 65535 and b = (2**16 >> 7) - 0x17.F)\x01\xda\x05print)'
    b'\x04\xda\x05guess\xda\x1abirth_year_minus_the_guess\xda\x01a\xda\x01b'
    b'\xa9\x00r\t\x00\x00\x00\xfa\x1f<ipython-input-27-d329bfeabe88>\xda\x05'
    b'claim\x05\x00\x00\x00s\x16\x00\x00\x00\x04\x01\x04\x01\x08\x03\x08'
    b'\x01\n\x01\x08\x02\x08\xfc\x10\x06\x04\x01\x08\x02\x04\x01'
)



cc = marshal.loads(code)
dis.dis(cc)

# Hint 0: N ever give up.
# Hint 1: What is the birth year of the person who inspired the name given to the members of the Cartesi community?
guess_and_birth_year_minus_the_guess = types.FunctionType(cc, globals(), "claim")


def hex_to_string(hex_value):
    """
    Decodes a hex string into a regular string.
    """
    return bytes.fromhex(hex_value[2:]).decode("utf-8")


def string_to_hex(string_value):
    """
    Encodes a string as a hex string.
    """
    return "0x" + string_value.encode("utf-8").hex()


def send_notice(notice: str) -> None:
    send_post("notice", notice)


def send_report(report: str) -> None:
    send_post("report", report)


def send_post(endpoint, json_data) -> None:
    response = requests.post(rollup_server + f"/{endpoint}", json=json_data)
    logger.info(
        f"/{endpoint}: Received response status {response.status_code} body {response.content}")


def handle_advance(data):
    logger.info(
        f"Receiving advance request with data {hex_to_string(data['payload'])} from {data['metadata']['msg_sender']}")
    binary = hex_to_string(data['payload'])
    json_data = json.loads(binary)
    try:
        if guess_and_birth_year_minus_the_guess(json_data["guess"], json_data["birth_year_minus_the_guess"]):
            logger.info("-----------------------SUCCESS-----------------------")
            notice_payload = {"payload": string_to_hex(
                f'Congratulations {data["metadata"]["msg_sender"]}! You have solved the challenge!')}
            send_notice(notice_payload)
            return "accept"
        else:
            raise ValueError("Wrong answer from " + data["metadata"]["msg_sender"])
    except Exception as e:
        msg = f"Error {e} processing data {data}"
        logger.error(f"{msg}\n{traceback.format_exc()}")
        send_report({"payload": string_to_hex(msg)})
        return "reject"


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
