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




    /*------------------
        Dashboard
    --------------------*/
    $(".modal").on("hidden.bs.modal", function(){
        $(".modal-body1").html("");
    })

    $('#plans').change(function () {
        console.log($(this).val())
        
        if ($(this).val() == 2000) {
            $('.msg-box').css("display", "block");

             
             document.getElementById('rio').innerText = '5%'
             //document.getElementById('price').innerText = '$100'
             

        }
        else if ($(this).val() == 5000) {
            $('.msg-box').css("display", "block");

             
             document.getElementById('rio').innerText = '5%'
             //document.getElementById('price').innerText = '$200'
             

        }
        else if ($(this).val() == 10000) {
            $('.msg-box').css("display", "block");

             
             document.getElementById('rio').innerText = '5%'
             //document.getElementById('price').innerText = '$300'
             

        }
    })

    $(".package_form").submit(function(event){
        event.preventDefault();
         
        console.log('checked')


      $.ajax({
            type: "POST",
            url: "/packages/purchase/",
            data: {
                pack_name:$('#plans').val(),
                 csrfmiddlewaretoken: csrftoken,
            },
            beforeSend: function() {
                document.getElementById('spineer').style.visibility = "visible";
                document.getElementById('purchase-span').innerText = 'processing'
            },
            success: function(data) {
                document.getElementById("response-msg").innerText = data.user
                setTimeout(function(){ window.location.reload(); },1300);
                 console.log(data)
 
 
            },
            complete: function() {
                document.getElementById('spineer').style.visibility = "hidden";
                document.getElementById('purchase-span').innerText = 'Done'
            },
        });
    });



    $(".wihdraw_form").submit(function(event){
        event.preventDefault();
        console.log($('#amount').val())
         
       


      $.ajax({
            type: "POST",
            url: "/withdraw/",
            data: {
                bank_name:$('#bank-name').val(),
                acc_name:$('#acct-name').val(),
                acc_num:$('#acct-num').val(),
                amount:$('#amount').val(),
                 csrfmiddlewaretoken: csrftoken,
            },
            beforeSend: function() {
                document.getElementById('with-spineer').style.visibility = "visible";
                document.getElementById('with-span').innerText = 'processing'
            },
            success: function(data) {
                document.getElementById("response-msg-with").innerText = data.user
                setTimeout(function(){ window.location.reload(); },1300);
                 console.log(data)
 
 
            },
            complete: function() {
                document.getElementById('with-spineer').style.visibility = "hidden";
                document.getElementById('with-span').innerText = 'Done'
                
            },
        });
    });

    $(".ref_form").submit(function(event){
        event.preventDefault();
         
        

      $.ajax({
            type: "POST",
            url: "/Ref/withdraw/",
            data: {
                ref_bank_name:$('#ref-bank-name').val(),
                ref_acc_name:$('#ref-acct-name').val(),
                ref_acc_num:$('#ref-acct-num').val(),
                  csrfmiddlewaretoken: csrftoken,
            },
            beforeSend: function() {
                document.getElementById('ref-spineer').style.visibility = "visible";
                document.getElementById('ref-span').innerText = 'processing'
            },
            success: function(data) {
                document.getElementById("response-msg-ref").innerText = data.user
                setTimeout(function(){ window.location.reload(); },1300);
                 console.log(data)
 
 
            },
            complete: function() {
                document.getElementById('ref-spineer').style.visibility = "hidden";
                document.getElementById('ref-span').innerText = 'Done'
            },
        });
    });
    
   /* $('.copy').click(function () {
        var copyText = document.getElementById("myInput");
      
         
        copyText.select();
        copyText.setSelectionRange(0, 99999);  
      
       
        document.execCommand("copy");
      
         
        alert("Copied the text: " + copyText.value);
    })*/

    /*$('.copyicon').click(function ()  {
        var copyText = document.getElementById("myInput");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        
        var tooltip = document.getElementById("myTooltip");
         
      })*/
     
    
     function outFunc() {
        var tooltip = document.getElementById("myTooltip");
        tooltip.innerHTML = "Copy to clipboard";
      }


      /* contact us */
      $(".contact_form_sub").submit(function(event){
        event.preventDefault();
        
      $.ajax({
            type: "POST",
            url: "/contact/message/",
            data: {
                name:$('#name').val(),
                email:$('#email').val(),
                message:$('#message').val(),
                  csrfmiddlewaretoken: csrftoken,
            },
            beforeSend: function() {
                document.getElementById('contact-spineer').style.visibility = "visible";
                document.getElementById('contact-span').innerText = 'processing'
                $("#contact-btn").addClass("disabled");
            },
            success: function(data) {
                document.getElementById("response-msg-contact").innerText = data.user
                setTimeout(function(){ window.location.reload(); },1300);
                 console.log(data)
 
 
            },
            complete: function() {
                document.getElementById('contact-spineer').style.visibility = "hidden";
                document.getElementById('contact-span').innerText = 'Done'
                
            },
        });
    });
    
     
    
    
    
      const price = document.querySelectorAll('.time');
         price.forEach((prc) => {
             const timer = prc.getAttribute('data-time')
             const userId = prc.getAttribute('data-userid')
             const packId = prc.getAttribute('data-packId')
            //console.log(timer)
                const eventS = Date.parse(timer)
                //console.log(eventS)
                // Update the count down every 1 second
                var x = setInterval(function() {
    
                // Get today's date and time
                var now = new Date().getTime();
    
                // Find the distance between now and the count down date
                var distance = eventS - now;
    
                // Time calculations for days, hours, minutes and seconds
                var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
                // Output the result in an element with id="demo"
                //prc.innerText = days + "d " + hours + "h "
                //+ minutes + "m " + seconds + "s ";
    
                // If the count down is over, write some text
                if (distance < 0) {
                    clearInterval(x);
                    //console.log('done')
                     credit_user(userId,packId)
                 }
                }, 1000);
      });
    
    
    
    function credit_user(user_id,packk_id) {
    
        $.ajax({
                type: "POST",
                url: "/Credit/user/",
                data: {
                    user: user_id,
                    pack : packk_id,
                     csrfmiddlewaretoken: csrftoken,
                },
                /*beforeSend: function() {
                    document.getElementById('spineer').style.visibility = "visible";
                    document.getElementById('purchase-span').innerText = 'processing'
                },*/
                success: function(data) {
                    //document.getElementById("response-msg").innerText = data.user
                    //setTimeout(function(){ window.location.reload(); },1300);
                     //console.log(data)
     
     
                },
                /*complete: function() {
                    document.getElementById('spineer').style.visibility = "hidden";
                    document.getElementById('purchase-span').innerText = 'Done'
                },*/
            });
    }
    
     

 });

 