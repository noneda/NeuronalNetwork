import os
import datetime

# Matplotlib backend for headless environments
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image


def generate_predictions_chart(preds, user: int, uploads_dir: str | None = None) -> str:

    preds_list = list(preds) if preds is not None else []
    if len(preds_list) == 0:
        raise ValueError("No predictions provided")

    xs = [float(p.prompt) for p in preds_list]
    ys = [float(p.response) for p in preds_list]

    pairs = sorted(zip(xs, ys), key=lambda t: t[0])
    xs_sorted, ys_sorted = zip(*pairs)

    if uploads_dir is None:
        uploads_dir = os.path.join(os.getcwd(), "uploads")

    os.makedirs(uploads_dir, exist_ok=True)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename_png = f"predictions_user_{user}_{timestamp}.png"
    filename_webp = f"predictions_user_{user}_{timestamp}.webp"

    png_path = os.path.join(uploads_dir, filename_png)
    webp_path = os.path.join(uploads_dir, filename_webp)

    plt.figure(figsize=(6, 4))
    plt.plot(xs_sorted, ys_sorted, marker="o", linestyle="-", color="#2b8cbe")
    plt.title(f"Predictions for user {user}")
    plt.xlabel("Hours studied")
    plt.ylabel("Predicted note")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close()

    try:
        img = Image.open(png_path)
        img.save(webp_path, format="WEBP", quality=85)
        try:
            os.remove(png_path)
        except Exception:
            pass
        return webp_path
    except Exception:
        return png_path
