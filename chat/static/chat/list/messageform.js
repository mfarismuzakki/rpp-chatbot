class MessageForm
{
    constructor()
    {

    }


    sendMessage()
    {
        let btn = document.getElementById('btn_submit');
        btn.addEventListener('click', () => 
        {
            let recipient = document.getElementById('recipient').value;
            let message = document.getElementById('message').value;
        })



    }


}


new MessageForm();