# Height Estimation from an Image

A small, interactive Python tool that estimates a person's height using a
known-height object in the same photograph. Select the person's full height,
then select the full height of a reference object (for example, a door).

![Project avatar](assets/project-avatar.svg)

## How it works

The estimate uses the proportional relationship below:

```text
person height = person pixels / reference pixels × reference height
```

For a useful result, photograph the person and the reference object at roughly
the same distance from the camera, keep the camera level, and select their
full visible heights. This is an approximation; perspective, tilted cameras,
and inaccurate selections all affect the result.

## Requirements

- Python 3.10 or newer
- An OpenCV build with desktop GUI support

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

Provide an image and the reference object's actual height in metres:

```bash
python height_estimation.py path/to/photo.jpg --reference-height 2.032
```

The application will ask you to draw two boxes in order:

1. The person, from feet to head.
2. The reference object, from bottom to top.

Drag a rectangle and press **Enter** or **Space** to accept it. Press **Esc**
to cancel. The annotated result is shown in a new window and also printed in
metres and centimetres.

See [examples/README.md](examples/README.md) for a concrete setup.

## Project layout

```text
.
├── height_estimation.py    # interactive command-line application
├── requirements.txt        # Python dependency
├── examples/               # usage notes
└── assets/                 # project visual assets
```

## Limitations

This is not a calibrated camera or computer-vision pose-estimation system. It
does not compensate for lens distortion or perspective, so avoid using it for
medical, legal, or safety-critical measurements.

## License

No license has been specified. Add a license file before distributing or
reusing the code.
