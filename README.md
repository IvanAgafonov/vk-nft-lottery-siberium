## VK-NFT-Lottery-Siberium

Сервис доступен по адресу https://vk.com/app51712830.

# Описание задачи

Сделать пробный сервис для проведения розыгрышей, раздач, лотерей с
помощью блокчейна Siberium на базе VK mini apps.

**Проблема**: в крупных розыгрышах от игроков
требуется доверие к организаторам для проверки результатов и
честного распределения шансов среди всех участников. С помощью
 блокчейна и смарт-контрактов каждый сможет проверить на какой адрес и когда поступил
тот или иной билет, а за счет идентификации в ВК определить и конкретного человека. 
Также с помощью генерации псевдослучайных чисел в смарт-контракте
удостовериться, что выигрышный билет выбран действительно случайно. 
И при желании гарантированно получить выигрыш в токенах сети через смарт-контракт.

В рамках данного проекта были допущения: 
1. используется один адрес смарт контракта токена ERC-721 с одним владельцем
2. каждый пользователей VK может получить один билет на любой
адрес в сети Siberium
3. функциональность сведена к минимуму - минту и просмотру NFT по адресу
4. функциональность для организатора отсутствует
5. генерация случайных чисел с выбором победителя 
и выплата призов производится вовне.


# Описание бизнес-процесса

В теории организатор приходит в сервис с желанием провести розыгрыш, выбирает нужные параметры:
количество билетов, сроки проведения, призы, требования к участникам и прочее. Организатору предаставляются уникальные коды для минтинга NFT в сервисы, которые он затем
раздает участникам. Которые в свою очередь авторизируясь через сервис получают NFT билеты на свои
кошельки. К окончанию проведения происходит снапшот кошельков, выбор победителя и раздача призов.


# Архитектура решения

### блокчейн
solidity 0.8.19,
openzeppelin,
ipfs

### backend

python 3.10
    - Flask, Web3, Sqlite

### frontend

react, vkontakte/vkui

# Финансовая оценка проекта

Потенциально любые физлица, компании, которые
проводят розыгрыши своей продукции в социальных сетях, как например
"баллы от Магнита за вступление в группу Вк", могут использовать сервис и платить отчисления
за проведение розыгрышей.



# Команда и контакты

Ivan Agafonov - developer - [github](https://github.com/IvanAgafonov) - [telegram](https://t.me/Foodfox_Ivan_Hashcodev)

# Инструкция

Для блокчейна.
1. Опубликовать смарт-контракт *data/LotteryNFT.sol*  в сети.

Для backend.
1. Заполнить *data/config.ini*.
2. Выполнить``flask run`` или ``python app.py``.

Для frontend.
1. ``npm start``.

