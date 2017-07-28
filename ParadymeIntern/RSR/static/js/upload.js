/**
 * Created by Abhishek on 25/07/17.
 */


function myfunction()
    {
        var div=document.getElementById('space');

        var input=getElement('input','file','docfile',true,'docfile');
        div.appendChild(input);

        var label=getElement('label',"","","","",'First Name:\t','firstname');
        div.appendChild(label);

        var firstname=getElement('input','text','firstname',true);
        div.appendChild(firstname);

        div.appendChild(getElement('label','','','','',' Last Name:\t'));

        var lastname=getElement('input','text','lastname',true,'lastname');
        div.appendChild(lastname);

        div.appendChild(getElement('label','','','','','Select Type:\t'));

        var select=getElement('select',"",'type',true,'select');
        select.setAttribute('class','type');
        div.appendChild(select);

        select.appendChild(getElement('option','','','','','None','',''));
        select.appendChild(getElement('option','','','','','Prospective Intern','','Prospective Intern'));
        select.appendChild(getElement('option','','','','','Prospective Employee','','Prospective Employee'));
        select.appendChild(getElement('option','','','','','Intern','','Intern'));
        select.appendChild(getElement('option','','','','','Employee','','Employee'));

        var cancel=getElement('button','','','','cancel','Cancel');
        div.appendChild(cancel);
        cancel.addEventListener('click',function () {
            cancelNode(cancel);
        });

        document.getElementById('uploadbtn').setAttribute('value','Upload All');
    }
function getElement(element,type,name,required,id,innerhtml,lfor,value)
{
    value=typeof value!=='undefined'? value:"";

    var variable=document.createElement(element);
    variable.setAttribute('type',type);
    variable.setAttribute('name',name);
    variable.required=required;
    variable.id=id;
    variable.innerHTML=innerhtml;
    variable.setAttribute('for',lfor);
    variable.setAttribute('value',value);
    return variable;
}

function cancelNode(childnode)
{
    var outer=childnode.parentNode;
    var childlist=outer.childNodes;
    var index=0;
    for(var i=0;i<childlist.length;i++)
    {
        if(childnode.isSameNode(childlist[i]))
            index=i;
    }
    for(i=index;i>=index-7;i--)
    {
        outer.removeChild(childlist[i]);
    }
    if(outer.hasChildNodes()===false)
    {
        document.getElementById('uploadbtn').setAttribute('value','Upload');
    }
}