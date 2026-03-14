#!/bin/bash
sphinx-apidoc --remove-old --force -o ./src/api/ ../../multiplied ../../multiplied/tests/* ../../multiplied/core/dtypes/*
