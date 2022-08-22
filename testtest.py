from testmain import main


def test_main_even_simpler(capsys):
    main(["--name", "Jürgen"])
    captured = capsys.readouterr()
    assert captured.out == "Hello Jürgefn\n"


if __name__ == '__main__':
    test_main_even_simpler()
    main()
    # main(['--name', 'Jürgen'])
