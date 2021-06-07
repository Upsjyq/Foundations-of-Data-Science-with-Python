from IPython.core.display import display, Javascript, HTML


def display_questions_dynamic_old(url, num=1_000_000, shuffle_questions=False, shuffle_answers=True):
    
    script_start="element.setAttribute('data-shufflequestions', '"+str(shuffle_questions) + "');";
    script_start+="element.setAttribute('data-shuffleanswers', '"+str(shuffle_answers) + "');";
    script_start+="element.setAttribute('data-numquestions', '"+str(num) + "');";
    script_start+='''
    
    //console.log(element);
    
    // Make a random ID
    function makeid(length) {
        var result           = [];
        var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
          result.push(characters.charAt(Math.floor(Math.random() *  charactersLength)));
       }
       return result.join('');
    }
    
    // Choose a random subset of an array. Can also be used to shuffle the array
    function getRandomSubarray(arr, size) {
        var shuffled = arr.slice(0), i = arr.length, temp, index;
        while (i--) {
            index = Math.floor((i + 1) * Math.random());
            temp = shuffled[index];
            shuffled[index] = shuffled[i];
            shuffled[i] = temp;
        }
        return shuffled.slice(0, size);
    }
    
    
    function check() {
        var id=this.id.split('-')[0];

        //console.log("In check(), id="+id);
        //console.log(event.srcElement.id)           
        //console.log(event.srcElement.dataset.correct)   
        //console.log(event.srcElement.dataset.feedback)

        var answers= event.srcElement.parentElement.children;
        //console.log(answers);
        
        // Split behavior based on multiple choice vs many choice:
        var fb = document.getElementById("fb"+id);
        if (fb.dataset.numcorrect==1) {
            for (var i = 0; i < answers.length; i++) {
                var child=answers[i];
                child.style.background="#fafafa";
            }



            fb.textContent=event.srcElement.dataset.feedback;
            if (event.srcElement.dataset.correct=="true")   {
                console.log("Correct action");
                event.srcElement.style.background="#d8ffc4";
                fb.style.color="#009113";
            } else {
                console.log("Error action");
                event.srcElement.style.background="#ffe8e8";
                fb.style.color="#DC2329";
            }
        }
        else {
            //console.log("Many choice not implemented yet");
            var reset = false;
            if (event.srcElement.dataset.correct=="true" )   {
                if (event.srcElement.dataset.answered<=0) {
                    if (fb.dataset.answeredcorrect<0) {
                        fb.dataset.answeredcorrect=1;
                        reset=true;
                    } else {
                       fb.dataset.answeredcorrect++;
                    }
                    if (reset) {
                        for (var i = 0; i < answers.length; i++) {
                            var child=answers[i];
                            child.style.background="#fafafa";
                            child.dataset.answered=0;
                        }
                    }
                    event.srcElement.style.background="#d8ffc4";
                    event.srcElement.dataset.answered=1;
                    fb.style.color="#009113";

                }
            } else {
                if (fb.dataset.answeredcorrect>0) {
                    fb.dataset.answeredcorrect=-1;
                    reset=true;
                } else {
                   fb.dataset.answeredcorrect--;
                }

                if (reset) {
                    for (var i = 0; i < answers.length; i++) {
                        var child=answers[i];
                        child.style.background="#fafafa";
                        child.dataset.answered=0;
                    }
                }
                event.srcElement.style.background="#ffe8e8";
                fb.style.color="#DC2329";
            }


            var numcorrect=fb.dataset.numcorrect;
            var answeredcorrect=fb.dataset.answeredcorrect;
            if (answeredcorrect>=0) {
                fb.textContent=event.srcElement.dataset.feedback + " ["  + answeredcorrect + "/" + numcorrect + "]";
            } else {
                fb.textContent=event.srcElement.dataset.feedback + "["  + 0 + "/" + numcorrect + "]";
            }


        }

        

    }
    
    function parse (json) {
        var shuffle_questions=element.dataset.shufflequestions;
        var num_questions=element.dataset.numquestions;
        var shuffle_answers=element.dataset.shuffleanswers;
        
        if (num_questions>json.length) {
            num_questions=json.length;
        }
        
        var questions;
        if ( (num_questions<json.length) || (shuffle_questions=="True") ) {
            //console.log(num_questions+","+json.length);
            questions=getRandomSubarray(json, num_questions);
        } else {
            questions=json;
        }
    
        //console.log("SQ: "+shuffle_questions+", NQ: " + num_questions + ", SA: ", shuffle_answers);
        questions.forEach((qa, index, array) => {
            //console.log(qa.question); 

            var id = makeid(8);
            //console.log(id);


            // Create Div to contain question and answers
            var iDiv = document.createElement('div');
            iDiv.id = 'quizWrap'+id+index;
            iDiv.style='max-width: 600px; margin: 0 auto;padding-bottom: 30px;';
            element.appendChild(iDiv);
            // iDiv.innerHTML=qa.question;

            // Create div to contain question part
            var qDiv = document.createElement('div');
            qDiv.id="quizQn"+id+index;
            qDiv.style='padding: 20px;color: #fafafa;font-size: 20px;border-radius: 10px; background: #6F78FF;';
            //qDiv.innerHTML=qa.question;
            qDiv.textContent=qa.question;
            iDiv.append(qDiv);

            // Create div to contain answer part
            var aDiv = document.createElement('div');
            aDiv.id="quizAns"+id+index;
            aDiv.style="margin: 10px 0; display: grid; grid-template-columns: auto auto;grid-gap: 10px;";
            iDiv.append(aDiv);
            
            var num_correct=0;
            
            var shuffled;
            if (shuffle_answers=="True") {
                //console.log(shuffle_answers+" read as true");
                shuffled=getRandomSubarray(qa.answers, qa.answers.length);
            } else {
                //console.log(shuffle_answers+" read as false");
                shuffled=qa.answers;
            }
        


            
            shuffled.forEach((item, index, ans_array) => {
                //console.log(answer);
                
                // Make input element
                var inp = document.createElement("input");
                inp.type="radio";
                inp.id="quizo"+id+index;
                inp.style="display:none;";
                aDiv.append(inp);
                
                //Make label for input element
                var lab = document.createElement("label");
                lab.style="background: #fafafa; border: 1px solid #eee;  border-radius: 10px; padding: 10px; font-size: 16px; cursor: pointer; text-align: center;";
                lab.id=id+ '-' +index;
                lab.onclick=check;
                lab.textContent=item.answer;
                
                // Set the data attributes for the answer
                lab.setAttribute('data-correct', item.correct);
                if (item.correct) {
                    num_correct++;
                }
                lab.setAttribute('data-feedback', item.feedback);
                lab.setAttribute('data-answered', 0);

                aDiv.append(lab);
                
                
            });
            
            //Make div for feedback
            var fb = document.createElement("div");
            fb.id="fb"+id;
            fb.style="font-size: 20px;text-align:center;";
            fb.setAttribute("data-answeredcorrect", 0);
            fb.setAttribute("data-numcorrect", num_correct);
            iDiv.append(fb);


        });
    }


            fetch("'''
    script_end='''")
      .then(response => response.json())
      .then(json => parse(json));

    
      '''
    javascript=script_start + url + script_end
    display(Javascript(javascript))

def display_questions_dynamic(url, num=1_000_000, shuffle_questions=False, shuffle_answers=True):

    mydiv='<div id="testDIV" data-shufflequestions="' + str(shuffle_questions) +'"'
    mydiv+=' data-shuffleanswers="' + str(shuffle_answers) +'"'
    mydiv+=' data-numquestions="' + str(num) +'">'
    
    
    script='<script type="text/Javascript">'
    
    script+='var mydiv=document.getElementById("testDIV");'
    script+='console.log(mydiv);'
    
    #display(HTML(mydiv + script))
    #return

    script+='''
    //console.log(element);
    
    // Make a random ID
    function makeid(length) {
        var result           = [];
        var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
          result.push(characters.charAt(Math.floor(Math.random() *  charactersLength)));
       }
       return result.join('');
    }
    
    // Choose a random subset of an array. Can also be used to shuffle the array
    function getRandomSubarray(arr, size) {
        var shuffled = arr.slice(0), i = arr.length, temp, index;
        while (i--) {
            index = Math.floor((i + 1) * Math.random());
            temp = shuffled[index];
            shuffled[index] = shuffled[i];
            shuffled[i] = temp;
        }
        return shuffled.slice(0, size);
    }
    
    
    function check() {
        var id=this.id.split('-')[0];

        //console.log("In check(), id="+id);
        //console.log(event.srcElement.id)           
        //console.log(event.srcElement.dataset.correct)   
        //console.log(event.srcElement.dataset.feedback)

        var answers= event.srcElement.parentElement.children;
        //console.log(answers);
        
        // Split behavior based on multiple choice vs many choice:
        var fb = document.getElementById("fb"+id);
        if (fb.dataset.numcorrect==1) {
            for (var i = 0; i < answers.length; i++) {
                var child=answers[i];
                child.style.background="#fafafa";
            }



            fb.textContent=event.srcElement.dataset.feedback;
            if (event.srcElement.dataset.correct=="true")   {
                console.log("Correct action");
                event.srcElement.style.background="#d8ffc4";
                fb.style.color="#009113";
            } else {
                console.log("Error action");
                event.srcElement.style.background="#ffe8e8";
                fb.style.color="#DC2329";
            }
        }
        else {
            //console.log("Many choice not implemented yet");
            var reset = false;
            if (event.srcElement.dataset.correct=="true" )   {
                if (event.srcElement.dataset.answered<=0) {
                    if (fb.dataset.answeredcorrect<0) {
                        fb.dataset.answeredcorrect=1;
                        reset=true;
                    } else {
                       fb.dataset.answeredcorrect++;
                    }
                    if (reset) {
                        for (var i = 0; i < answers.length; i++) {
                            var child=answers[i];
                            child.style.background="#fafafa";
                            child.dataset.answered=0;
                        }
                    }
                    event.srcElement.style.background="#d8ffc4";
                    event.srcElement.dataset.answered=1;
                    fb.style.color="#009113";

                }
            } else {
                if (fb.dataset.answeredcorrect>0) {
                    fb.dataset.answeredcorrect=-1;
                    reset=true;
                } else {
                   fb.dataset.answeredcorrect--;
                }

                if (reset) {
                    for (var i = 0; i < answers.length; i++) {
                        var child=answers[i];
                        child.style.background="#fafafa";
                        child.dataset.answered=0;
                    }
                }
                event.srcElement.style.background="#ffe8e8";
                fb.style.color="#DC2329";
            }


            var numcorrect=fb.dataset.numcorrect;
            var answeredcorrect=fb.dataset.answeredcorrect;
            if (answeredcorrect>=0) {
                fb.textContent=event.srcElement.dataset.feedback + " ["  + answeredcorrect + "/" + numcorrect + "]";
            } else {
                fb.textContent=event.srcElement.dataset.feedback + "["  + 0 + "/" + numcorrect + "]";
            }


        }

        

    }
    
    function parse (json) {
        var mydiv=document.getElementById("testDIV");
        console.log(mydiv);
        console.log(mydiv.dataset);
        var shuffle_questions=mydiv.dataset.shufflequestions;
        var num_questions=mydiv.dataset.numquestions;
        var shuffle_answers=mydiv.dataset.shuffleanswers;
        
        if (num_questions>json.length) {
            num_questions=json.length;
        }
        
        var questions;
        if ( (num_questions<json.length) || (shuffle_questions=="True") ) {
            //console.log(num_questions+","+json.length);
            questions=getRandomSubarray(json, num_questions);
        } else {
            questions=json;
        }
    
        console.log("SQ: "+shuffle_questions+", NQ: " + num_questions + ", SA: ", shuffle_answers);
        questions.forEach((qa, index, array) => {
            //console.log(qa.question); 

            var id = makeid(8);
            //console.log(id);


            // Create Div to contain question and answers
            var iDiv = document.createElement('div');
            iDiv.id = 'quizWrap'+id+index;
            iDiv.style='max-width: 600px; margin: 0 auto;padding-bottom: 30px;';
            mydiv.appendChild(iDiv);
            // iDiv.innerHTML=qa.question;

            // Create div to contain question part
            var qDiv = document.createElement('div');
            qDiv.id="quizQn"+id+index;
            qDiv.style='padding: 20px;color: #fafafa;font-size: 20px;border-radius: 10px; background: #6F78FF;';
            //qDiv.innerHTML=qa.question;
            qDiv.textContent=qa.question;
            iDiv.append(qDiv);

            // Create div to contain answer part
            var aDiv = document.createElement('div');
            aDiv.id="quizAns"+id+index;
            aDiv.style="margin: 10px 0; display: grid; grid-template-columns: auto auto;grid-gap: 10px;";
            iDiv.append(aDiv);
            
            var num_correct=0;
            
            var shuffled;
            if (shuffle_answers=="True") {
                //console.log(shuffle_answers+" read as true");
                shuffled=getRandomSubarray(qa.answers, qa.answers.length);
            } else {
                //console.log(shuffle_answers+" read as false");
                shuffled=qa.answers;
            }
        


            
            shuffled.forEach((item, index, ans_array) => {
                //console.log(answer);
                
                // Make input element
                var inp = document.createElement("input");
                inp.type="radio";
                inp.id="quizo"+id+index;
                inp.style="display:none;";
                aDiv.append(inp);
                
                //Make label for input element
                var lab = document.createElement("label");
                lab.style="background: #fafafa; border: 1px solid #eee;  border-radius: 10px; padding: 10px; font-size: 16px; cursor: pointer; text-align: center;";
                lab.id=id+ '-' +index;
                lab.onclick=check;
                lab.textContent=item.answer;
                
                // Set the data attributes for the answer
                lab.setAttribute('data-correct', item.correct);
                if (item.correct) {
                    num_correct++;
                }
                lab.setAttribute('data-feedback', item.feedback);
                lab.setAttribute('data-answered', 0);

                aDiv.append(lab);
                
                
            });

            //Make div for feedback
            var fb = document.createElement("div");
            fb.id="fb"+id;
            fb.style="font-size: 20px;text-align:center;";
            fb.setAttribute("data-answeredcorrect", 0);
            fb.setAttribute("data-numcorrect", num_correct);
            iDiv.append(fb);


        });
    }


            fetch("'''
    script_end='''")
      .then(response => response.json())
      .then(json => parse(json));


    </script>
      '''
    javascript=script + url + script_end
    display(HTML(mydiv + javascript))
