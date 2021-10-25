#!/bin/bash
./flaschen-taschen/server/ft-server -d \
    --led-rows=64 \
    --led-cols=64 \
    --led-chain=1 \
    --led-parallel=1 \
    --led-gpio-mapping=adafruit-hat-pwm \
    --led-brightness=80 \
    --led-limit-refresh=200 \
    --led-pixel-mapper="Rotate:180" \
    --led-slowdown-gpio=0