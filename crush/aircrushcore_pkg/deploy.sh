#!/bin/bash

python3 -m build
ls dist
echo python3 -m twine upload --repository testpypi dist/*

# __token__
echo pypi-AgENdGVzdC5weXBpLm9yZwIkYzhkYjk1N2EtN2Q2OC00ZjY1LThhNGUtMmRhNDJiYjYyZDE5AAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiAqMHmOhjfzUY21HjQ7aIP7AJxGzV0NvLMeBWV7SFPMpw
echo pip install -i https://test.pypi.org/simple/ aircrushcore