$(document).ready(function () {

    $('#submit-first-name').click(function (e) {
        const button = $(e.currentTarget)
        const user_id = button.data('source')
        $.ajax({
            type: 'POST',
            url: '/edit-first-name',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': user_id,
                'first_name': $('#first-name-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-last-name').click(function (e) {
        const button = $(e.currentTarget)
        const user_id = button.data('source')
        $.ajax({
            type: 'POST',
            url: '/edit-last-name',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': user_id,
                'last_name': $('#last-name-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-email').click(function (e) {
        const button = $(e.currentTarget)
        const user_id = button.data('source')
        $.ajax({
            type: 'POST',
            url: '/edit-email',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': user_id,
                'email': $('#email-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    
    $('#submit-phone').click(function (e) {
        const button = $(e.currentTarget)
        const user_id = button.data('source')
        $.ajax({
            type: 'POST',
            url: '/edit-phone',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': user_id,
                'phone_number': $('#phone-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-password').click(function (e) {
        const button = $(e.currentTarget)
        const user_id = button.data('source')
        $.ajax({
            type: 'POST',
            url: '/edit-password',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': user_id,
                'password': $('#password-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#goToBubble').click(function (e) {
   
        const button = $(e.currentTarget)
        const user_id = button.data('source')

        
        
        $.ajax({
            type: 'GET',
            url: '/user-bubbles/' + user_id,
            contentType: 'application/json;charset=UTF-8',
            
            success: function (res) {
                window.location.href = '/user-bubbles/' + user_id;
            },
            error: function () {
                console.log('Error');
                
            }
        });
    });

    $('#goToInteractions').click(function (e) {
   
        const button = $(e.currentTarget)
        const user_id = button.data('source')

        var today = new Date();
        var dd = today.getDate();

        var mm = today.getMonth()+1; 
        var yyyy = today.getFullYear();
        if(dd<10) 
        {
            dd='0'+dd;
        } 

        if(mm<10) 
        {
            mm='0'+mm;
        } 
        
        $.ajax({
            type: 'GET',
            url: '/interactions/' + user_id,
            contentType: 'application/json;charset=UTF-8',
            
            success: function (res) {
                window.location.href = '/interactions/' + user_id;
            },
            error: function () {
                console.log('Error');
                
            }
        });
    });


    $('#goToTests').click(function (e) {
   
        const button = $(e.currentTarget)
        const user_id = button.data('source')

        
        
        $.ajax({
            type: 'GET',
            url: '/search-test/' + user_id,
            contentType: 'application/json;charset=UTF-8',
            
            success: function (res) {
                window.location.href = '/search-test/' + user_id;
            },
            error: function () {
                console.log('Error');
                
            }
        });
    });

    $('#goToVaccinations').click(function (e) {
   
        const button = $(e.currentTarget)
        const user_id = button.data('source')

        
        
        $.ajax({
            type: 'GET',
            url: '/search-vaccination/' + user_id,
            contentType: 'application/json;charset=UTF-8',
            
            success: function (res) {
                window.location.href = '/search-vaccination/' + user_id;
            },
            error: function () {
                console.log('Error');
                
            }
        });
    });

    $('#goToStats').click(function (e) {
   
        const button = $(e.currentTarget)
        const user_id = button.data('source')

        
        
        $.ajax({
            type: 'GET',
            url: '/user-statistics/' + user_id,
            contentType: 'application/json;charset=UTF-8',
            
            success: function (res) {
                window.location.href = '/user-statistics/' + user_id;
            },
            error: function () {
                console.log('Error');
                
            }
        });
    });

});
