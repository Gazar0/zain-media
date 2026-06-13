import { sendEmail } from './_email.js'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })

  try {
    const { name, email, phone, service, details } = req.body || {}
    if (!name || !email || !phone || !service || !details) {
      return res.status(400).json({ error: 'جميع الحقول المطلوبة يجب ملؤها' })
    }

    const body = `
      <div dir="rtl" style="font-family:Arial;max-width:600px;margin:auto;padding:20px;">
        <h2 style="color:#7C3AED;">طلب عرض سعر جديد</h2>
        <table style="width:100%;border-collapse:collapse;">
          <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">العميل:</td><td>${name}</td></tr>
          <tr style="background:#f9f9f9;"><td style="padding:8px;font-weight:bold;color:#7C3AED;">البريد:</td><td>${email}</td></tr>
          <tr><td style="padding:8px;font-weight:bold;color:#7C3AED;">الهاتف:</td><td>${phone}</td></tr>
          <tr style="background:#f9f9f9;"><td style="padding:8px;font-weight:bold;color:#7C3AED;">الخدمة:</td><td>${service}</td></tr>
        </table>
        <div style="margin-top:16px;padding:16px;background:#f5f3ff;border-radius:8px;">
          <h4 style="color:#7C3AED;margin:0 0 8px;">التفاصيل:</h4>
          <p style="margin:0;line-height:1.7;">${details}</p>
        </div>
      </div>`

    await sendEmail('memogazar049@gmail.com', `طلب عرض سعر جديد من ${name}`, body)
    return res.json({ success: true, message: 'تم إرسال طلب عرض السعر بنجاح' })
  } catch (err) {
    return res.status(500).json({ error: 'فشل إرسال البريد' })
  }
}
