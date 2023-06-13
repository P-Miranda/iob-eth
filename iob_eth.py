#!/usr/bin/env python3

import os
import sys

from iob_module import iob_module
from setup import setup

# Submodules
from iob_utils import iob_utils
from iob_clkenrst_portmap import iob_clkenrst_portmap
from iob_clkenrst_port import iob_clkenrst_port
from iob_reg import iob_reg
from iob_reg_e import iob_reg_e


class iob_eth(iob_module):
    name='iob_eth'
    version="V0.20"
    flows="sim emb lint fpga doc"
    setup_dir=os.path.dirname(__file__)

    @classmethod
    def _run_setup(cls):
        # Hardware headers & modules
        iob_module.generate("iob_s_port")
        iob_utils.setup()
        iob_clkenrst_portmap.setup()
        iob_clkenrst_port.setup()
        iob_reg.setup()
        iob_reg_e.setup()

        cls._setup_confs()
        cls._setup_ios()
        cls._setup_regs()
        cls._setup_block_groups()

        # Verilog modules instances
        # TODO

        # Copy sources of this module to the build directory
        super()._run_setup()

        # Setup core using LIB function
        setup(cls)



    @classmethod
    def _setup_confs(cls):
        super()._setup_confs([
            # Macros

            # Parameters
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "`IOB_ETH_SWREG_ADDR_W",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "ETH_MAC_ADDR",
                "type": "P",
                "val": "`ETH_MAC_ADDR",
                "min": "NA",
                "max": "NA",
                "descr": "Instance MAC address",
            },
            {
                "name": "PHY_RST_CNT",
                "type": "P",
                "val": "20'hFFFFF",
                "min": "NA",
                "max": "NA",
                "descr": "Reset counter value",
            },
        ])

    @classmethod
    def _setup_ios(cls):
        cls.ios += [
            {"name": "iob_s_port", "descr": "CPU native interface", "ports": []},
            {"name": "iob_m_port", "descr": "Native master memory interface", "ports": []},
            {
                "name": "general",
                "descr": "General Interface Signals",
                "ports": [
                    {
                        "name": "clk_i",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "System clock input",
                    },
                    {
                        "name": "arst_i",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "System reset, asynchronous and active high",
                    },
                    {
                        "name": "cke_i",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "System clock enable signal",
                    },
                    {
                        "name": "inta_o",
                        "type": "O",
                        "n_bits": "1",
                        "descr": "Interrupt Output A",
                    },
                ],
            },
            {
                "name": "phy",
                "descr": "PHY Interface Ports",
                "ports": [
                    {
                        "name": "MTxClk",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "Transmit Nibble or Symbol Clock. The PHY provides the MTxClk signal. It operates at a frequency of 25 MHz (100 Mbps) or 2.5 MHz (10 Mbps). The clock is used as a timing reference for the transfer of MTxD[3:0], MtxEn, and MTxErr.",
                    },
                    {
                        "name": "MTxD",
                        "type": "O",
                        "n_bits": "4",
                        "descr": "Transmit Data Nibble. Signals are the transmit data nibbles. They are synchronized to the rising edge of MTxClk. When MTxEn is asserted, PHY accepts the MTxD.",
                    },
                    {
                        "name": "MTxEn",
                        "type": "O",
                        "n_bits": "1",
                        "descr": "Transmit Enable. When asserted, this signal indicates to the PHY that the data MTxD[3:0] is valid and the transmission can start. The transmission starts with the first nibble of the preamble. The signal remains asserted until all nibbles to be transmitted are presented to the PHY. It is deasserted prior to the first MTxClk, following the final nibble of a frame.",
                    },
                    {
                        "name": "MTxErr",
                        "type": "O",
                        "n_bits": "1",
                        "descr": "Transmit Coding Error. When asserted for one MTxClk clock period while MTxEn is also asserted, this signal causes the PHY to transmit one or more symbols that are not part of the valid data or delimiter set somewhere in the frame being transmitted to indicate that there has been a transmit coding error.",
                    },
                    {
                        "name": "MRxClk",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "Receive Nibble or Symbol Clock. The PHY provides the MRxClk signal. It operates at a frequency of 25 MHz (100 Mbps) or 2.5 MHz (10 Mbps). The clock is used as a timing reference for the reception of MRxD[3:0], MRxDV, and MRxErr.",
                    },
                    {
                        "name": "MRxDv",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "Receive Data Valid. The PHY asserts this signal to indicate to the Rx MAC that it is presenting the valid nibbles on the MRxD[3:0] signals. The signal is asserted synchronously to the MRxClk. MRxDV is asserted from the first recovered nibble of the frame to the final recovered nibble. It is then deasserted prior to the first MRxClk that follows the final nibble.",
                    },
                    {
                        "name": "MRxD",
                        "type": "I",
                        "n_bits": "4",
                        "descr": "Receive Data Nibble. These signals are the receive data nibble. They are synchronized to the rising edge of MRxClk. When MRxDV is asserted, the PHY sends a data nibble to the Rx MAC. For a correctly interpreted frame, seven bytes of a preamble and a completely formed SFD must be passed across the interface.",
                    },
                    {
                        "name": "MRxErr",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "Receive Error. The PHY asserts this signal to indicate to the Rx MAC that a media error was detected during the transmission of the current frame. MRxErr is synchronous to the MRxClk and is asserted for one or more MRxClk clock periods and then deasserted.",
                    },
                    {
                        "name": "MColl",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "Collision Detected. The PHY asynchronously asserts the collision signal MColl after the collision has been detected on the media. When deasserted, no collision is detected on the media.",
                    },
                    {
                        "name": "MCrS",
                        "type": "I",
                        "n_bits": "1",
                        "descr": "Carrier Sense. The PHY asynchronously asserts the carrier sense MCrS signal after the medium is detected in a non-idle state. When deasserted, this signal indicates that the media is in an idle state (and the transmission can start).",
                    },
                    {
                        "name": "MDC",
                        "type": "O",
                        "n_bits": "1",
                        "descr": "Management Data Clock. This is a clock for the MDIO serial data channel.",
                    },
                    {
                        "name": "MDIO",
                        "type": "IO",
                        "n_bits": "1",
                        "descr": "Management Data Input/Output. Bi-directional serial data channel for PHY/STA communication.",
                    },
                ],
            },
        ]

    @classmethod
    def _setup_regs(cls):
        cls.regs += [
            {
                "name": "iob_eth",
                "descr": "IOb-Eth Software Accessible Registers.",
                "regs": [
                    {
                        "name": "MODER",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 40960,
                        "addr": 0,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Mode Register",
                    },
                    {
                        "name": "INT_SOURCE",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 4,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Interrupt Source Register",
                    },
                    {
                        "name": "INT_MASK",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 8,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Interrupt Mask Register",
                    },
                    {
                        "name": "IPGT",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 18,
                        "addr": 12,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Back to Back Inter Packet Gap Register",
                    },
                    {
                        "name": "IPGR1",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 12,
                        "addr": 16,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Non Back to Back Inter Packet Gap Register 1",
                    },
                    {
                        "name": "IPGR2",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 18,
                        "addr": 20,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Non Back to Back Inter Packet Gap Register 2",
                    },
                    {
                        "name": "PACKETLEN",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 4195840,
                        "addr": 24,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Packet Length (minimum and maximum) Register",
                    },
                    {
                        "name": "COLLCONF",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 61443,
                        "addr": 28,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Collision and Retry Configuration",
                    },
                    {
                        "name": "TX_BD_NUM",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 64,
                        "addr": 32,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Transmit Buffer Descriptor Number",
                    },
                    {
                        "name": "CTRLMODER",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 36,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Control Module Mode Register",
                    },
                    {
                        "name": "MIIMODER",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 100,
                        "addr": 40,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MII Mode Register",
                    },
                    {
                        "name": "MIICOMMAND",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 44,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MII Command Register",
                    },
                    {
                        "name": "MIIADDRESS",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 48,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MII Address Register. Contains the PHY address and the register within the PHY address",
                    },
                    {
                        "name": "MIITX_DATA",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 52,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MII Transmit Data. The data to be transmitted to the PHY",
                    },
                    {
                        "name": "MIIRX_DATA",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 56,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MII Receive Data. The data received from the PHY",
                    },
                    {
                        "name": "MIISTATUS",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 60,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MII Status Register",
                    },
                    {
                        "name": "MAC_ADDR0",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 64,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MAC Individual Address0. The LSB four bytes of the individual address are written to this register",
                    },
                    {
                        "name": "MAC_ADDR1",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 68,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "MAC Individual Address1. The MSB two bytes of the individual address are written to this register",
                    },
                    {
                        "name": "ETH_HASH0_ADR",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 72,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "HASH0 Register",
                    },
                    {
                        "name": "ETH_HASH1_ADR",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 76,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "HASH1 Register",
                    },
                    {
                        "name": "ETH_TXCTRL",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "addr": 80,
                        "log2n_items": 0,
                        "autologic": True,
                        "descr": "Transmit Control Register",
                    },
                ],
            }
        ]

    @classmethod
    def _setup_block_groups(cls):
        cls.block_groups += [
            iob_block_group(
                name = "host_if",
                description = "Host Interface",
                "blocks": [
                    iob_verilog_instance(
                        name = "IFC+CSR",
                        description = "Interface Controller (IFC), and Control and Status Registers (CSR)",
                    ),
                    iob_verilog_instance(
                        name = "Buffer Descriptors",
                        description = "Internal memory for Buffer Descriptors",
                    ),
                    iob_verilog_instance(
                        name = "TX Buffer",
                        description = "Internal storage for immediate frame transfer",
                    ),
                    iob_verilog_instance(
                        name = "RX Buffer",
                        description = "Internal storage for immediate frame reception",
                    ),
                    iob_verilog_instance(
                        name = "DMA",
                        description = "Direct Memory Access module. Writes received frames to memory and reads frames for transfer.",
                    ),
                ],
            ),
            iob_block_group(
                name = "mii_management",
                description = "MII Management module",
                "blocks": [
                    iob_verilog_instance(
                        name = "Clock generator",
                        description = "Divides system clock into slower clock for PHY interface",
                    ),
                    iob_verilog_instance(
                        name = "Operation Controller",
                        description = "Control MII read and write operations",
                    ),
                    iob_verilog_instance(
                        name = "Shift Registers",
                        description = "Enable serial (MII side) to parallel (host side) communication",
                    ),
                    iob_verilog_instance(
                        name = "Output Control",
                        description = "Control MDIO signal. Can be either input or output",
                    ),
                ],
            ),
            iob_block_group(
                name = "tx_module",
                description = "Frame transfer module",
                "blocks": [
                    iob_verilog_instance(
                        name = "Status signals",
                        description = "Read and write transfer related signals from CSR and Buffer Descriptors",
                    ),
                    iob_verilog_instance(
                        name = "Frame Pad",
                        description = "Add padding to outgoing frames",
                    ),
                    iob_verilog_instance(
                        name = "CRC",
                        description = "Calculate Cyclic Redundancy Check (CRC) for outgoing frame",
                    ),
                    iob_verilog_instance(
                        name = "Data nibble",
                        description = "Convert data bytes to nibbles",
                    ),
                    iob_verilog_instance(
                        name = "PHY Signals",
                        description = "Output PHY TX signals",
                    ),
                ],
            ),
            iob_block_group(
                name = "rx_module",
                description = "Frame reception module",
                "blocks": [
                    iob_verilog_instance(
                        name = "Status signals",
                        description = "Read and write reception related signals from CSR and Buffer Descriptors",
                    ),
                    iob_verilog_instance(
                        name = "CRC",
                        description = "Verify Cyclic Redundancy Check (CRC) for incoming frame",
                    ),
                    iob_verilog_instance(
                        name = "Preamble removal",
                        description = "Detect and remove incoming frame preamble",
                    ),
                    iob_verilog_instance(
                        name = "Data Assembly",
                        description = "Convert PHY RX signal into data bytes",
                    ),
                ],
            ),
        ]
