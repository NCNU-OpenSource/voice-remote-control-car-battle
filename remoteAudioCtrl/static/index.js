let recognizer;

function listen() {
     if (recognizer.isListening()) {
     recognizer.stopListening();
     toggleButtons(true);
     document.getElementById('listen').textContent = 'Listen';
     return;
   }
   // Array of words that the recognizer is trained to recognize.
   const words = recognizer.wordLabels();
   recognizer.listen(({scores}) => {
   // Turn scores into a list of (score,word) pairs.
   scores = Array.from(scores).map((s, i) => ({score: s, word: words[i]}));
   // Find the most probable word.
   scores.sort((s1, s2) => s2.score - s1.score);
   document.querySelector('#console').textContent = scores[0].word;
   let sendURL = "";
   switch(scores[0].word)
   {
   	case 'forward_zh':
		   sendURL = '/background_forward';
		   break;
	
   	case 'backward_zh':
		   sendURL = '/background_backward';
		   break;
	
   	case 'left_zh':
		   sendURL = '/background_left';
		   break;
	
   	case 'right_zh':
		   sendURL = '/background_right';
		   break;
   };
   $.getJSON(sendURL);
 }, {probabilityThreshold: 0.8, overlapFactor:0.85});
}

function toggleButtons(enable) {
 document.querySelectorAll('button').forEach(b => b.disabled = !enable);
}

function flatten(tensors) {
 const size = tensors[0].length;
 const result = new Float32Array(tensors.length * size);
 tensors.forEach((arr, i) => result.set(arr, i * size));
 return result;
}

async function app() {
// recognizer = speechCommands.create('BROWSER_FFT', null, 'https://raw.githubusercontent.com/efficacy38/test_LSA_audio_predict/main/model.json', 'https://raw.githubusercontent.com/efficacy38/test_LSA_audio_predict/main/metadata.json');  en+zh
    recognizer = speechCommands.create('BROWSER_FFT', null, 'https://raw.githubusercontent.com/efficacy38/test__2/main/model.json', 'https://raw.githubusercontent.com/efficacy38/test__2/main/metadata.json');
 await recognizer.ensureModelLoaded();
}

app();
