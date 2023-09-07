$(document).ready(function () {
    $('#testr-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes
        const modal = $(this)
        if (taskID === 'New Test') {
            modal.find('.modal-title').text(taskID)
            $('#testr-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Test ' + taskID)
            $('#testr-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.testr-control').val('');
        } else {
            modal.find('.testr-control').val('');
        }
    })


    $('#submit-testr').click(function (event) {
        const button = $(event.currentTarget)
        const tID = $('#testr-form-display').attr('taskID');
        const user_id = button.data('source');
        console.log($('#testr-modal').find('.testr-control').val())

        $.ajax({
            type: 'POST',
            url: tID ? '/edit-test/' + tID +'/'+ user_id : '/create-test/'+user_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'result': $('#result').val(),
                'test_date': $('#test_date').val(),
                'user_id': user_id
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

    $('.removet').click(function () {
        const remove = $(this)

        $.ajax({
            type: 'POST',
            url: '/delete-test/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    
    $('#search-test').click(function(){
        const search_string = document.getElementById('key-test').value;
        $.ajax({
            type: 'GET',
            url:'/search-test/'+search_string ,
            // data: JSON.stringify({
            //     'key': $('#key').val()
            // }),
            success: function (res) {
                console.log(res.response)
                window.location.href = '/search-test/'+search_string;
            },
            error: function () {
                console.log('Error');
            }

        });

    });

});