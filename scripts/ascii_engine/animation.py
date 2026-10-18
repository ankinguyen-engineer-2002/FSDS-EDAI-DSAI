#!/usr/bin/env python3
"""
Flagship Multi-Frame / CSS Steps() Data-Flow Animation Registry for the Monodraw+Durdraw Engine.
"""
from typing import Dict, Set

# Flagship diagrams across the 4 topics that showcase live Durdraw-style data-flow pulse on connectors
FLAGSHIP_ANIMATED_DIAGRAMS: Set[str] = {
    # F01 Linux Fundamentals
    "linux:0.1",
    "linux:1.2",
    "linux:3.1",
    "linux:3.2",
    # F02 Python Fundamentals
    "python:0.1",
    "python:1.2",
    "python:2.2",
    "python:4.2",
    # F03 Database Fundamentals
    "db:0.1",
    "db:1.2",
    "db:3.2",
    "db:4.2",
    # F04 Web API
    "api:0.1",
    "api:1.5",
    "api:2.4",
    "api:3.4",
    "api:5.1",
    # F06 Containerization & Orchestration
    "container:0.1",
    "container:2.1",
    "container:3.2",
    "container:4.2",
    # D01 Ingestion Layer
    "ingestion:0.1",
    "ingestion:2.4",
    "ingestion:3.3",
    "ingestion:4.1",
    "ingestion:5.2",
    # D02 Storage & Data Platform
    "storage:0.1",
    "storage:1.1",
    "storage:6.1a",
    "storage:7.1a",
    # D04 Transformation Layer (Stream - Flink)
    "flink:0.1",
    "flink:1.2",
    "flink:2.2",
    "flink:3.3",
    "flink:5.3",
    "flink:6.2",
    # D05 Consumption Layer (DW, OLAP, Feast)
    "consumption:0.1",
    "consumption:2.3",
    "consumption:3.1",
    "consumption:4.2",
    "consumption:5.4",
    # D06 Orchestration & Governance (Airflow & DataHub)
    "orchestration:0.1",
    "orchestration:1.1",
    "orchestration:2.4",
    "orchestration:3.2",
    "orchestration:5.2",
}


def is_flagship_animated(topic_prefix: str, diag_key: str) -> bool:
    return f"{topic_prefix}:{diag_key}" in FLAGSHIP_ANIMATED_DIAGRAMS
