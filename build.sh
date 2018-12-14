#!/bin/bash
pyinstaller --noconfirm --log-level INFO \
                --onefile --windowed \
                --clean \
                pongame.spec
