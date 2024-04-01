from telebot.handler_backends import StatesGroup, State

# Факт о дате число - date_fact_day
# Факт о дате месяц - date_fact_month
# Факт о числе - math_fact_num
# Факт со случайным числом левая граница - random_fact_min
# Факт со случайным числом правая граница - random_fact_max
# Интересный факт связанный с числом - trivia_fact_num
# Пользователь выбирает нужно ли ему искать другое число - trivia_fact_another_num
# Пользователь выбрал округлять в большую сторону - trivia_fact_round_high
# Пользователь выбрал округлять в меньшую сторону - trivia_fact_round_low
# Событие произошедшее в заданном году - year_fact_year


class NumbersFacts(StatesGroup):
    date_fact_month = State()
    date_fact_day = State()
    math_fact_num = State()
    random_fact_min = State()
    random_fact_max = State()
    trivia_fact_num = State()
    trivia_fact_no = State()
    trivia_fact_another_num = State()
    trivia_fact_round_high = State()
    trivia_fact_round_low = State()
    year_fact_year = State()
