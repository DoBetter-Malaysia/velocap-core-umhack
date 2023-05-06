from linkedin_api import Linkedin


def test_constructor():
    api = Linkedin("email", "password")
    results = api.search({"keywords": "Supplycart"})
    print(results)

test_constructor()