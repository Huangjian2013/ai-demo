export default {
  async fetch(request, env) {
    // 如果是 OPTIONS 请求，返回 CORS 头
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Allow-Credentials': 'true',
        },
      });
    }

    // 确保是 POST 请求
    if (request.method !== 'POST') {
      return new Response('Only POST requests are allowed', { 
        status: 405, 
        headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
      },
    });
    }

        // 检查 Content-Type 是否是 multipart/form-data
        const contentType = request.headers.get('Content-Type') || '';
        if (!contentType.includes('multipart/form-data')) {
          return new Response('Expected multipart/form-data', { status: 400 });
        }
    
        // 解析 form-data 内容
        const formData = await request.formData();
        const imageFile = formData.get('image');
    
        if (!imageFile) {
          return new Response('No image file found in the request', { status: 400 });
        }
    
        // 将图像数据转为 ArrayBuffer
        const arrayBuffer = await imageFile.arrayBuffer();
        const inputs = {
          image: [...new Uint8Array(arrayBuffer)],
        };


    // 调用AI模型
    const response = await env.AI.run('@cf/microsoft/resnet-50', inputs);

    // 返回响应，包含 CORS 头
    return new Response(JSON.stringify({ inputs: { image: [] }, response }), {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json',
      },
    });
  },
};
