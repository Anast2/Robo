launch:

- node:
    pkg: "rooted_encoder"
    exec: "encoder_virtual"
    name: "encoder_node"
    param:
    -
      name: "DEVICENAME"
      value: "/dev/ttyServo"
    -
      name: "BAUDRATE"
      value: "1_000_000"
