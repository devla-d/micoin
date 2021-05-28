$(document).ready(function () {
      /* csrf token */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $('.pay-btn').click(function () {
        $.ajax({
            type: "POST",
            url: "/Dashboard/Admin/Wihdrawals/approve/",
            data: {
                pk:$('.withdraw').attr('data-pk'),
                user_pk:$('.username').attr('data-user'),
                invest_id:$('.investment-pk').attr('id'),
                   csrfmiddlewaretoken: csrftoken,
            },
            //beforeSend: function() {
                //document.getElementById('ref-spineer').style.visibility = "visible";
                //document.getElementById('ref-span').innerText = 'processing'
            //},
            success: function(data) {
                document.getElementById("response-msg-ref").innerText = data.user
                setTimeout(function(){ window.location.reload(); },1300);
                 console.log(data)
 
 
            },
            //complete: function() {
                //document.getElementById('ref-spineer').style.visibility = "hidden";
                //document.getElementById('ref-span').innerText = 'Done'
            //},
        });
   
    })

    $('.refpay-btn').click(function () {
        $.ajax({
            type: "POST",
            url: "/Dashboard/Admin/RefWihdrawals/approve/",
            data: {
                pk:$('.refwithdraw').attr('data-pk'),
                user_pk:$('.refusername').attr('data-user'),
               
                   csrfmiddlewaretoken: csrftoken,
            },
            //beforeSend: function() {
                //document.getElementById('ref-spineer').style.visibility = "visible";
                //document.getElementById('ref-span').innerText = 'processing'
            //},
            success: function(data) {
                document.getElementById("response-msg-ref").innerText = data.user
                setTimeout(function(){ window.location.reload(); },1300);
                 console.log(data)
 
 
            },
            //complete: function() {
                //document.getElementById('ref-spineer').style.visibility = "hidden";
                //document.getElementById('ref-span').innerText = 'Done'
            //},
        });
   
    })


})