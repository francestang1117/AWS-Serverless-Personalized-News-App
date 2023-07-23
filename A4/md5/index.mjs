import fetch from 'node-fetch';
import crypto from 'crypto';


export const handler = async (event) => {
  const { value, course_uri } = event;

  const md5_hashed = crypto.createHash('md5').update(value).digest('hex');
  const payload = {
    banner: 'B00899622',
    result: md5_hashed,
    arn: process.env.AWS_LAMBDA_FUNCTION_INVOKED_ARN,
    action: 'md5',
    value: value,
  };

  try {
    const response = await fetch(course_uri, {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: { 'Content-Type': 'application/json' },
    });

    return {
      statusCode: response.status,
      body: JSON.stringify(await response.json()),
    };
  } catch (e) {
    return {
      statusCode: 400,
      body: JSON.stringify({ errorMessage: 'An  error' + e.message + 'occurred.' }),
    };
  }
};

