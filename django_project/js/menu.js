$(document).ready( function () {
    $('#tnx_table').DataTable();
} );


//function toggleMenuBar(e) {
//    e.preventDefault();
//    $("#wrapper").toggleClass("toggled");
//}


function getTransactions() {
    $.ajax({
        url: "/transaction",
        type: 'GET',
        async: true,
        success: function (result) {
            // console.log(result);
            renewTable(result);
        }
    });
}

function addTransaction() {
    $("#model_title").html("Add new transaction");
    tableHtml =
        `<table class="table table-striped">
            <tbody>
                <tr>
                    <td>Date</td>
                    <td><input type="text" placeholder="<date>" size="35" name="date"></td>
                </tr>
                <tr>
                    <td>Amount</td>
                    <td><input type="text" placeholder="<amount>" size="35" name="amount"></td>
                </tr>
                <tr>
                    <td>Spender</td>
                    <td><input type="text" placeholder="<spender>" size="35" name="spender"></td>
                </tr>
                <tr>
                    <td>Type</td>
                    <td><input type="text" placeholder="<type>" size="35" name="type"></td>
                </tr>
                <tr>
                    <td>Category</td>
                    <td><input type="text" placeholder="<category>" size="35" name="category"></td>
                </tr>
                <tr>
                    <td>Description</td>
                    <td><input type="text" placeholder="<description>" size="35" name="description"></td>
                </tr>
            </tbody>
        </table>`;
    $("#modal_body").html(tableHtml);
    $("#modal_error").addClass("invisible");
    $("#main_modal").modal();
    $("#modal_save").html("Add transaction");
    $("#modal_save").unbind().click(() => addTransactionCall());
}

function addTransactionCall() {
    let modal_form = $("#modal_form");
    let form_data =
        modal_form.serializeArray().reduce(function(obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});


    console.log("making request to add transaction");
    console.log(JSON.stringify(form_data));
    $.ajax({
        url: "/transaction",
        type: 'PUT',
        contentType: "application/json",
        data: JSON.stringify(form_data),
        async: true,
        complete: function (result) {
            // console.log(result);
            requestOk = result.status === 200;
            modalUpdate(requestOk, result.body);
        }
    });
}

function modalUpdate(success, errorMessage = "Error with modal update") {
    if (success) {
        console.log("Closing modal...");
        setTimeout(function() { getTransactions() }, 250);
        $("#main_modal").modal('hide');
    } else {
        displayModalError(errorMessage);
    }
}

function displayModalError(message) {
    let errorElement = $("#modal_error");
    errorElement.removeClass("invisible");
    let errorMessage = message === "" ? "Empty error message" : message;
    errorElement.html(errorMessage);
}

function renewTable(data) {
    let table = $("#tnx_table");
    let tnx_body = $("#tnx_body");
    table.dataTable().fnDestroy(); // Destroy the previous table
    tnx_body.empty();
    html = "";
    for (row in data) {
        html += createRow(data[row])
    }
    tnx_body.html(html);
    table.DataTable();

}

function createRow(row) {
    html = "<tr>";
    html += "<td>" + row.date +  "</td>";
    html += "<td>" + row.amount +  "</td>";
    html += "<td></td>";
    html += "<td>" + row.category +  "</td>";
    html += "<td>" + row.spender +  "</td>";
    html += "<td>" + row.desc +  "</td>";
    html += "</tr>";
    return html;
}


});
