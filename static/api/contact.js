import { sendEmail } from './_email.js'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  try {
    const { name, email, phone, message } = req.body || {}
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'الاسم، البريد، والرسالة مطلوبون' })
    }

    const body = `
      <div dir="rtl" style="font-family:Arial;max-width:600px;margin:auto;padding:20px;">
        <h2 style="color:#7C3AED;">رسالة جديدة من موقع Zain Media</h2>
        <table style="width:100%;border-collapse:collapse;">
          <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">الاسم:</td><td>${name}</td></tr>
          <tr style="background:#f9f9f9;"><td style="padding:8px;font-weight:bold;color:#7C3AED;">البريد:</td><td>${email}</td></tr>
          <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">الهاتف:</td><td>${phone || '—'}</td></tr>
        </table>
        <div style="margin-top:16px;padding:16px;background:#f5f3ff;border-radius:8px;">
          <h4 style="color:#7C3AED;margin:0 0 8px;">الرسالة:</h4>
          <p style="margin:0;line-height:1.7;">${message}</p>
        </div>
      </div>`

    await sendEmail('memogazar049@gmail.com', `رسالة جديدة من ${name} — Zain Media`, body)
    return res.json({ success: true, message: 'تم إرسال الرسالة بنجاح' })
  } catch (err) {
    return res.status(500).json({ error: 'فشل إرسال البريد' })
  }
}
