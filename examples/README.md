# Example: estimating height with a door

Suppose `family-photo.jpg` contains a person standing next to a standard door
whose measured height is 2.032 metres (80 inches).

```bash
python height_estimation.py family-photo.jpg --reference-height 2.032
```

When prompted, draw one rectangle tightly around the person and a second one
tightly around the door. If the selected person is 690 pixels tall and the
door is 760 pixels tall, the program reports:

```text
Estimated height: 1.84 m (184 cm)
```

For best results, place the person beside the door rather than in front of it,
and take the photo straight-on.
