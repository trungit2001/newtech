from database import run_pipeline

def main():
    engine, _ = run_pipeline()
    print(engine)


if __name__ == "__main__":
    main()