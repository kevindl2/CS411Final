$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#vaccination-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes
        const modal = $(this)
        if (taskID === 'New vaccination') {
            modal.find('.modal-title').text(taskID)
            $('#vaccination-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Vaccination ' + taskID)
            $('#vaccination-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.vac-control').val('');
        } else {
            modal.find('.vac-control').val('');
        }
    })


    $('#submit-vaccination').click(function (event) {
        const button = $(event.currentTarget)
        const tID = $('#vaccination-form-display').attr('taskID');
        const user_id = button.data('source')
        console.log(user_id)
        console.log($('#vaccination-modal').find('.vac-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit-vaccination/' + tID +'/'+user_id: '/create-vaccination/'+user_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': $('#user_id').val(),
                'vaccine_brand': $('#vaccine_brand').val(),
                'vaccine_date': $('#vaccine_date').val()
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

    $('.removev').click(function () {
        const remove = $(this)

        $.ajax({
            type: 'POST',
            url: '/delete-vaccination/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    
    $('#search').click(function(){
        const search_string = document.getElementById('key').value;
        $.ajax({
            type: 'GET',
            url:'/search-vaccination/'+search_string ,
            // data: JSON.stringify({
            //     'key': $('#key').val()
            // }),
            success: function (res) {
                console.log(res.response)
                window.location.href = '/search-vaccination/'+search_string;
            },
            error: function () {
                console.log('Error');
            }

        });

    });

    $('#searchQ').click(function(){
        const search_string = document.getElementById('keyQ').value;
        $.ajax({
            type: 'GET',
            url:'/searchQ/'+search_string ,
            // data: JSON.stringify({
            //     'key': $('#key').val()
            // }),
            success: function (res) {
                console.log(res.response)
                window.location.href = '/searchQ/'+search_string;
            },
            error: function () {
                console.log('Error');
            }

        });

    });

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


    $('#submit-testr').click(function () {
        const tID = $('#testr-form-display').attr('taskID');
        console.log($('#testr-modal').find('.testr-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit-test/' + tID : '/create-test',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'result': $('#result').val(),
                'test_date': $('#test_date').val(),
                'user_id': $('#user_id').val()
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

});