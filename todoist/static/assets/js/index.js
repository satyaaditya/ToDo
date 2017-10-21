function loadLists(){
    $.ajax({
        type: "GET",
        url: "/todo/index/lists/",
        //data : $("#formed").serialize(),
        success: function(result) {
            let cards = "";
            for(let i =0;i<result.length;i++)
            {
                cards +=
                    `<div class="auto card card-block">
                    <nav class="navbar navbar-toggleable-md bg-info">
                        <div class="container">
                            <div class="navbar-translate">
                                <a class="navbar-brand" href="#">
                                    ` + result[i].name + `
                                </a>
                            </div>
                            <div class="collapse navbar-collapse justify-content-end">
                                <ul class="navbar-nav">
                                    <li class="nav-item">
                                        <a class="nav-link" href="#" onclick="scrollToDownload()">
                                            <i class="fa fa-pencil"></i>
                                            <p>Edit</p>
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="#" onclick="deleteList(` + result[i].id + `)">
                                            <i class="fa fa-trash-o"></i>
                                            <p>Delete</p>
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a onclick="open_modal(`+result[i].id+`)"  class="nav-link" href="#" data-toggle="modal" data-id = "` + result[i].id + `" data-target="#itemModal">
                                            <i class="fa fa-plus"></i>
                                            <p>Add Item</p>
                                        </a>
                                    </li>

                                </ul>
                            </div>
                        </div>
                    </nav>
                    <div id="itemContainer` + result[i].id + `">
                    </div>`;

                // result tables
                getItemsForList(result[i].id);
                cards += `</div>`;
            }
            $("#cardContainer").html(cards);

        },
        error: function(result) {
            alert('error');
        }
    });
}

function showSuccess(msg){

    let alert = `<div class="alert alert-success" role="alert">
                <div class="container">
                    <div class="alert-icon">
                        <i class="now-ui-icons ui-2_like"></i>
                    </div>
                    <strong>Success:</strong> `+msg+`
                    <button type="button"  class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">
                            <i class="now-ui-icons ui-1_simple-remove"></i>
                        </span>
                    </button>
                </div>
            </div>`;

    $("#alertContainer").html(alert);
}

function deleteList(id){
    $.ajax({
        type: "DELETE",
        url : "todo/lists/" + id + "/",
        success: function(result) {
            showSuccess("List deleted successfully");
            loadLists();
        },
        error: function(result){
            alert('error');
        }
    });
}
function deleteItem(id){
    $.ajax({
        type: "DELETE",
        url : "todo/items/" + id + "/",
        success: function(result) {
            showSuccess("Item deleted successfully");
            loadLists();
        },
        error: function(result){
            alert('error');
        }
    });
}
function open_modal(id)
{
    $("#listId").val(id);
}

$("#createNewItem").submit(function(e) {
    let data = $("#createNewItem").serialize();
    //alert(data);
    $.ajax({
        type: "POST",
        url: "/todo/lists/items/",
        data : data,
        success: function(result) {
            showSuccess("created succesfully");
            $("#itemModal").modal('hide');
            loadLists();
        },
        error: function(result) {
            // alert(result);
            $("#error").html(JSON.stringify(result));
        }
    });
    e.preventDefault();
});

function getItemsForList(listId)
{
    let containerName = "#itemContainer"+listId;
    let cards = "";

    $.ajax({
        type: "GET",
        url: "/todo/lists/" + listId + "/items/",
        success: function(itemsData) {
            if(itemsData.length>0)
            //
                cards += `<div class="card-block" style="height: 150px;overflow-y: scroll;">
                              <table class="table table-striped style = "height:150px;overflow-y: scroll;" ">
                                <thead>
                                    <tr>
                                      <th width="50%">Items</th>
                                      <th width = "30%">Completed</th>
                                      <th width="20%" colspan="2" style="text-align: center;">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>`;
            else
                cards += `No records yet!`;
            for(let j=0;j<itemsData.length;j++){
                cards += `<tr>
                              <td scope="row">` + itemsData[j].description + `</td>
                              <td>` + itemsData[j].completed + `</td>
                              <td><button class = "btn btn-warning btn-icon btn-icon-mini" onclick = editListItem(` + itemsData[j].id + `)><i class="fa fa-pencil"></i></button></td>
                              <td><button class = "btn btn-danger btn-icon btn-icon-mini" onclick="deleteItem(` + itemsData[j].id + `)"><i class="fa fa-trash"></i></button></td></td>
                            </tr>`;

                //console.log("cards variable from ajax get : " + cards);
            }
            cards += `</tbody>
                        </table>                                    
                        </div>`;
            $(containerName).html(cards);
        },
        error: function(itemError) {
            //console.log("result from error : " + JSON.stringify(itemError));
        }
    });
}