import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

TOKEN = '7705205365:AAHqT9FMz2Gt2-zgTbYIaEBp_s7CpShJ2Eo'

QUESTIONS = [
    'аэропОрты', 'бАнты', 'бОроду', 'бухгАлтеров', 'вероисповЕдание', 'водопровОд', 'газопровОд', 'граждАнство', 'дефИс', 'дешевИзна',
    'диспансЕр', 'договорЁнность', 'докумЕнт', 'досУг', 'еретИк', 'жалюзИ', 'знАчимость', 'Иксы', 'каталОг', 'квартАл', 'киломЕтр', 'кОнусов',
    'корЫсть', 'крАны', 'кремЕнь', 'лЕкторов', 'лОктя', 'лыжнЯ', 'мЕстностей', 'намЕрение', 'нарОст', 'нЕдруг', 'недУг', 'некролОг', 'нЕнависть',
    'нефтепровОд', 'новостЕй', 'нОгтя', 'Отзыв (о книге)', 'отзЫв (посла из страны)', 'Отрочество', 'партЕр', 'портфЕль', 'пОручни', 'придАное',
    'призЫв', 'свЁкла', 'сирОты', 'созЫв', 'сосредотОчение', 'вернА', 'знАчимый', 'красИвее', 'красИвейший', 'кУхонный', 'дождалАсь', 'дозвонИтся',
    'дозИровать', 'ждалА', 'жилОсь', 'закУпорить', 'занЯть', 'заперлА', 'запломбировАть', 'защемИт', 'звалА', 'звонИт', 'вОвремя', 'дОверху', 'донЕльзя',
    'дОнизу', 'дОсуха', 'зАсветло', 'зАтемно', 'налИвший', 'нанЯвшийся', 'начАвший', 'нАчатый', 'низведЁнный', 'облегчЁнный', 'ободрЁнный', 'срЕдства','стАтуя',
    'столЯр','тамОжня','тОрты','тУфля','цемЕнт', 'цЕнтнер', 'цепОчка', 'шАрфы','шофЁр', 'экспЕрт','лгалА','лилА','лилАсь','навралА','наделИт', 'надорвалАсь',
    'назвалАсь','накренИтся', 'налилА','нарвалА','начАть','обзвонИт','облегчИть', 'облилАсь','обнялАсь', 'обогналА', 'ободралА','ободрИть','ободрИться',
    'обострИть', 'одолжИть', 'озлОбить', 'оклЕить', 'окружИт','опОшлить', 'освЕдомиться',  'отбылА', 'отдалА', 'откУпорить','отозвалАсь','перезвонИт',
    'перелилА','плодоносИть','довезЁнный', 'зАгнутый', 'зАнятый','зАпертый', 'заселЁнный','кормЯщий'
]

INCORRECT_OPTIONS = [
    'аэропортЫ', 'бантЫ', 'борОду', 'бухгалтерОв', 'вероисповедАние', 'водопрОвод', 'газопрОвод', 'грАжданство', 'дЕфис', 'дешевизнА',
    'диспАнсер', 'договОрённость', 'докУмент', 'дОсуг', 'Еретик', 'жАлюзи', 'значИмость', 'иксЫ', 'катАлог', 'квАртал', 'килОметр', 'конусОв',
    'кОрысть', 'крЕмень', 'лекторОв', 'локтЯ', 'лЫжня', 'местностЕй', 'намерЕние', 'нАрост', 'недрУг', 'нЕдуг', 'некрОлог', 'ненавИсть', 'нефтепрОвод',
    'нОвостей', 'ногтЯ', 'отзЫв (о книге)', 'Отзыв (посла из страны)', 'отрОчество', 'пАртер', 'пОртфель', 'порУчни', 'прИданое', 'прИзыв', 'свёклА', 'сИроты', 'сОзыв', 'сосредоточЕние',
    'вЕрна', 'значИмый', 'красивЕе', 'красивЕйший', 'кухОнный', 'дождАлась', 'дозвОнится', 'дозировАть', 'ждАла', 'жИлось', 'закупОрить', 'зАнять', 'зАперла',
    'запломбИровать', 'защЕмит', 'звАла', 'звОнит', 'воврЕмя', 'довЕрху', 'дОнельзя', 'донИзу', 'досУха', 'засвЕтло', 'затЕмно', 'нАливший', 'нАнявшийся',
    'нАчавший', 'начАтый', 'низвЕдённый', 'облЕгчённый', 'обОдрённый', 'средствА', 'статУя', 'стОляр',  'тортЫ','туфлЯ', 'цЕмент', 'центнЕр', 'цЕпочка',
    'шарфЫ', 'Эксперт','лгАла','лИла','лИлась','наврАла','надЕлит', 'надорвАлась','назвАлась','накрЕнится', 'налИла','нарвАла','нАчать','обзвОнит',
    'облЕгчить', 'облИлась','обнЯлась', 'обогнАла', 'ободрАла','обОдрить','обОдриться','обОстрить', 'одОлжить', 'озлобИть', 'оклеИть', 'окрУжит','опошлИть',
    'осведомИться',  'отбЫла', 'отдАла', 'откупОрить','отозвАлась','перезвОнит', 'перелИла','плодонОсить','загнУтый', 'занЯтый','запЕртый', 'засЕлённый','кОрмящий'
]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    message_text = (
        "Здравствуйте! Этот бот поможет вам проверить правильное ударение в словах.\n"
        "Доступные команды:\n"
        "/quiz — начать тест\n"
        "Чтобы начать, введите /quiz"
    )
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(message_text)
    elif hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(message_text)

async def quiz(update: Update, context):
    # Инициализация данных для пользователя
    context.user_data['score'] = 0
    context.user_data['question_indices'] = list(range(len(QUESTIONS)))
    random.shuffle(context.user_data['question_indices'])
    await send_question(update, context)

async def send_question(update: Update, context):
    """Отправка вопроса или финального результата."""
    if not context.user_data['question_indices']:
        score = context.user_data.get('score', 0)
        text = f"Тест завершен! Правильных ответов: {score} из {len(QUESTIONS)}."
        # Отправим сообщение с кнопкой "Начать заново"
        restart_button = InlineKeyboardButton("Начать заново", callback_data='restart')
        reply_markup = InlineKeyboardMarkup([[restart_button]])
        if hasattr(update, 'callback_query') and update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        elif hasattr(update, 'message') and update.message:
            await update.message.reply_text(text, reply_markup=reply_markup)
        return

    question_idx = context.user_data['question_indices'].pop()
    context.user_data['current_question'] = question_idx
    question_word = QUESTIONS[question_idx]
    correct_answer = question_word

    # собираем неправильные варианты, исключая правильный
    incorrects_pool = [opt for opt in INCORRECT_OPTIONS if opt.lower() != correct_answer.lower()]

    selected_wrong_options = []
    used_words = {correct_answer.lower()}
    attempts = 0
    max_attempts = 100

    while len(selected_wrong_options) < 3 and attempts < max_attempts:
        candidate = random.choice(incorrects_pool)
        candidate_word = candidate.lower()
        if candidate_word not in used_words:
            selected_wrong_options.append(candidate)
            used_words.add(candidate_word)
        attempts += 1

    # если не удалось подобрать 3 уникальных варианта
    if len(selected_wrong_options) < 3:
        remaining_needed = 3 - len(selected_wrong_options)
        remaining_options = [opt for opt in incorrects_pool if opt not in selected_wrong_options]
        selected_wrong_options.extend(random.sample(remaining_options, remaining_needed))

    options = selected_wrong_options + [correct_answer]
    random.shuffle(options)

    # создаем кнопки
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # отправляем сообщение
    if hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(
            text="Выберите правильное ударение в слове:",
            reply_markup=reply_markup
        )
    elif hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            text="Выберите правильное ударение:",
            reply_markup=reply_markup
        )

async def handle_answer(update: Update, context):
    """Обработка нажатий на кнопки."""
    query = update.callback_query
    await query.answer()

    if query.data == 'restart':
        # Начинаем заново
        await quiz(update, context)
        return

    selected = query.data
    current_idx = context.user_data.get('current_question')
    if current_idx is None:
        # если по какой-то причине вопрос не выбран
        await query.edit_message_text("Пожалуйста, начните тест командой /quiz.")
        return

    correct_answer = QUESTIONS[current_idx]

    if selected == correct_answer:
        # правильный ответ
        context.user_data['score'] = context.user_data.get('score', 0) + 1
        await send_question(update, context)
    else:
        # неправильный — завершение теста
        score = context.user_data.get('score', 0)
        text = (
            f"Неправильно! Тест завершен.\n\n"
            f"Правильных ответов: {score}.\n"
            f"Правильный ответ: '{QUESTIONS[current_idx]}'. Ваш ответ: '{selected}'."
        )
        # добавим кнопку "Начать заново"
        restart_button = InlineKeyboardButton("Начать заново", callback_data='restart')
        reply_markup = InlineKeyboardMarkup([[restart_button]])
        await query.edit_message_text(text, reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('quiz', quiz))
    app.add_handler(CallbackQueryHandler(handle_answer))
    app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())