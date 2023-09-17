const A = require('arcsecond');
const B = require('arcsecond-binary');

export async function parse(path) {
  const parser = A.sequenceOf([
    getRIFFChunk(),
    getFMTSubChunk(),
    getDATASubChunk(),
    // A.endOfInput,
  ]).map(([riff, fmt, data]) => ({
    riff,
    fmt,
    data
  }));

  const file = Bun.file(path);
  const output = parser.run(await file.arrayBuffer());
  if (output.isError) {
    console.error(output.error);
    // throw new Error(output.error);
  }

  return output;
}

function getRIFFChunk() {
  return A.sequenceOf([A.str('RIFF'), B.u32LE, A.str('WAVE')]);
}

function getFMTSubChunk() {
  return A.coroutine(function* () {
    const id = yield A.str('fmt ');
    const subChunk1Size = yield B.u32LE;
    const audioFormat = yield B.u16LE;
    const numChannels = yield B.u16LE;
    const sampleRate = yield B.u32LE;
    const byteRate = yield B.u32LE;
    const blockAlign = yield B.u16LE;
    const bitsPerSample = yield B.u16LE;

    const fmtChunkData = {
      id,
      subChunk1Size,
      audioFormat,
      numChannels,
      sampleRate,
      byteRate,
      blockAlign,
      bitsPerSample,
    };

    yield A.setData(fmtChunkData);
    return fmtChunkData;
  });
}

function getDATASubChunk() {
  return A.coroutine(function* () {
    const id = yield A.str('data');
    const size = yield B.u32LE;
    const fmtData = yield A.getData;
    const samples = size / fmtData.numChannels / (fmtData.bitsPerSample / 8);
    const channelData = Array.from({ length: fmtData.numChannels }, () => []);

    let sampleParser;
    if (fmtData.bitsPerSample === 8) {
      sampleParser = B.s8;
    } else if (fmtData.bitsPerSample === 16) {
      sampleParser = B.s16LE;
    } else if (fmtData.bitsPerSample === 32) {
      sampleParser = B.s32LE;
    } else {
      yield A.fail(`Unsupported bits per sample: ${fmtData.bitsPerSample}`);
    }

    for (let sampleIndex = 0; sampleIndex < samples; sampleIndex++) {
      for (let i = 0; i < fmtData.numChannels; i++) {
        const sampleValue = yield sampleParser;
        channelData[i].push(sampleValue);
      }
    }

    return {
      id,
      size,
      channelData,
    };
  });
}