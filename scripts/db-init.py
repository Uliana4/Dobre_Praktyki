from app.models import Base, get_engine


def main():
    engine = get_engine("movies.db")
    Base.metadata.create_all(engine)
    print("Baza movies.db z tabelami utworzona.")


if __name__ == "__main__":
    main()