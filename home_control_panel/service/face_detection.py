from facenet_pytorch import MTCNN


class FastMTCNN(object):
    """Fast MTCNN implementation."""

    def __init__(self, stride, min_confidence, resize=1, *args, **kwargs):
        """Constructor for FastMTCNN class.

        Arguments:
            stride (int): The detection stride. Faces will be detected every `stride` frames
                and remembered for `stride-1` frames.

        Keyword arguments:
            resize (float): Fractional frame scaling. [default: {1}]
            *args: Arguments to pass to the MTCNN constructor. See help(MTCNN).
            **kwargs: Keyword arguments to pass to the MTCNN constructor. See help(MTCNN).
        """
        self.stride = stride
        self.resize = resize
        self.min_confidence = min_confidence
        self.mtcnn = MTCNN(*args, **kwargs)

    def __call__(self, frame):
        """Detect face in frame using strided MTCNN."""
        boxes, probs = self.mtcnn.detect(frame)  # [::self.stride]
        face_detected = False
        for prob in probs:
            if prob is not None and prob * 100 > self.min_confidence:
                face_detected = True
                break

        return face_detected
