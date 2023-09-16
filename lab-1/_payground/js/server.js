const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const multer  = require('multer');
const upload = multer({ dest: 'uploads/' })
// const main = require('./main');

const A = require('arcsecond');
const B = require('arcsecond-binary');


const fs = require('fs');
const path = require('path');

eval(fs.readFileSync('/Users/tomas/Downloads/Making-WAVs-master/index.js')+'');

const app = express();
const port = 3000;

app.use(cors({ origin: '*' }));
// app.use(express.json({limit: '25mb'}));
// app.use(express.urlencoded({limit: '25mb'}));
app.use(express.static('public'));

// app.use(bodyParser.json({ limit: '10mb' }));
// app.use(bodyParser.urlencoded({ extended: true, limit: '10mb' }));

// nodemon
// Define your API endpoint
app.post('/api', upload.single('avatar'), async (req, res) => {
  // const result = await main(req.file.path)
  // console.log(result)
  // console.log(result.result.fmtSubChunk)

  function* myGenerator() {
    yield 'Hello';
    yield 'World';
  }

  const generator = myGenerator();
  let result = '';

  for (const value of generator) {
    result += value + ' ';
  }

  main();
  console.log('INNN');
  res.json({ message: result});
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

function main() {
  const file = fs.readFileSync("/Users/tomas/Downloads/Sounds/Angry_german.wav");
  // const file = fs.readFileSync(path.join(__dirname, './Angry_german.wav'));

  const riffChunkSize = B.u32LE.chain((size) => {
    if (size !== file.length - 8) {
      return A.fail(`Invalid file size: ${file.length}. Expected ${size}`);
    }
    return A.succeedWith(size);
  });

  const riffChunk = A.sequenceOf([A.str('RIFF'), riffChunkSize, A.str('WAVE')]);

  function* myGenerator () {
    const id = A.str('fmt ');
    const subChunk1Size = B.u32LE;

    return {
      id,
      subChunk1Size,
    };
  }

  const fmtSubChunk = A.coroutine(myGenerator);


  const parser = A.sequenceOf([
    riffChunk,
    fmtSubChunk,

  ]).map(([riffChunk, fmtSubChunk]) => {
    const generator = myGenerator();

    console.log("IN");
    // console.log(fmtSubChunk.run())

    for (const value of fmtSubChunk) {
      console.log(value); // This will print 'Hello' and then 'World' to the console
    }
    console.log("OUT")
    return {
      riffChunk,
      fmtSubChunk,
    }
  });

  const output = parser.run(file.buffer);
  if (output.isError) {
    throw new Error(output.error);
  }

  console.log(output.result);
}
