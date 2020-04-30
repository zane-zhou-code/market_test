from twilio.rest import Client
def sendMessage(toPhoneNumber, Msg):
    account_sid = 'AC6ef77fd2b0c11ea51b3c42ac75c5e97b' # 1 920 365 5958
    auth_token = '8642d3b7cbfd9b342dc7081d78d19117'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to='+86'+toPhoneNumber,
        from_='19203655958',
        body=Msg
    )
    print(message.sid)
Msg = '测试python程序'
sendMessage('13760214167', Msg)