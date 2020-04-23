/*global SudokuSolver _config*/

var SudokuSolver = window.SudokuSolver || {};
SudokuSolver.map = SudokuSolver.map || {};

(function homeScopeWrapper($) {
    var authToken;
    SudokuSolver.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = 'login.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = 'login.html';
    });
    
    function requestSolution(picture) {
        $.ajax({
            method: 'POST',
            url: _config.api.invokeUrl + '/ride',
            headers: {
                Authorization: authToken
            },
            data: picture,
            contentType: 'application/json',
            success: completeRequest,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured when requesting your unicorn:\n' + jqXHR.responseText);
            }
        });
    }

    function completeRequest(result) {

    }

    // Register click handler for #request button
    $(function onDocReady() {

        $('#sudokuPictureBtn').click(function() {
            requestSolution("");
        });
        
        $('#signOut').click(function() {
            SudokuSolver.signOut();
            
            alert("You have been signed out.");
            window.location = "login.html";
        });

        SudokuSolver.authToken.then(function updateAuthMessage(token) {
            if (token) {
                console.log(token);
            }
        });

        // if (!_config.api.invokeUrl) {
        //     $('#noApiMessage').show();
        // }
    });

}(jQuery));
