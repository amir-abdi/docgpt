from docgpt import model


def test_estimate_tokens():
    # this, ' ', is, /, a, +, 4
    assert model.estimate_num_tokens("this is/a+4") == int(7 * model.TOKEN_ESTIMATE_COEFF)
