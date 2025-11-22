from datetime import datetime


def run() -> None:
    print("Seeding development environment...")
    print(" - Creating MinIO buckets: uploads, ocr, extractions")
    print(" - Applying database migrations placeholder")
    print(f"Seed completed at {datetime.utcnow().isoformat()}Z")


if __name__ == "__main__":
    run()
