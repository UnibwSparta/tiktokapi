import sparta.tiktokapi


# If there are no other tests this one is needed -> otherwise pytest will fail
def test_package() -> None:
    sparta.tiktokapi
    assert True
