import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_project(dut):
    dut._log.info("Testing 8-bit AND circuit")

    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 1

    test_cases = [
        (0x00, 0x00),
        (0xFF, 0xFF),
        (0xFF, 0x00),
        (0xAA, 0x55),
        (0x36, 0x1C),
        (0x0F, 0x33),
        (0x81, 0x81),
        (0xF0, 0x0F),
    ]

    for a, b in test_cases:
        dut.ui_in.value = a
        dut.uio_in.value = b

        # Allow combinational logic to settle
        await Timer(2, unit="ns")

        expected = a & b
        actual = int(dut.uo_out.value)

        dut._log.info(
            f"{a:#04x} AND {b:#04x} = "
            f"{actual:#04x} (expected {expected:#04x})"
        )

        assert actual == expected, (
            f"Failed: {a:#04x} AND {b:#04x}: "
            f"got {actual:#04x}, expected {expected:#04x}"
        )

    dut._log.info("All AND tests passed!")
