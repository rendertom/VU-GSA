import * as audio from './audio.js';

const server = Bun.serve({
  port: 3000,
  async fetch(req) {
    const method = req.method;
    const url = new URL(req.url);

    if (method === 'GET' && url.pathname === '/') {
      return new Response(Bun.file('public/index.html'));
    }

    if (method === 'POST' && url.pathname === '/api') {
      const formdata = await req.formData();
      const file = formdata.get('file');
      if (!file) throw new Error('Must upload a profile picture.');

      const path = 'temp_file.wav';
      await Bun.write(path, file);

      const data = await audio.parse(path);
      return new Response(JSON.stringify(data));
    }

    return new Response('Not Found', { status: 404 });
  },
});

console.log(`Listening on http://localhost:${server.port}`);
