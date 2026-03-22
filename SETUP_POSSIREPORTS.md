# 🌐 Setup Guide: possireports.in

## Step 1: Buy Your Domain

### Option A: Buy on Namecheap (Recommended) ✅
1. Go to: https://www.namecheap.com
2. Search for: `possireports.in`
3. Add to cart (~$4.88/year for .in domains)
4. Complete checkout
5. Keep the DNS settings with Namecheap

### Option B: Buy on GoDaddy
1. Go to: https://www.godaddy.com
2. Search for: `possireports.in`
3. Add to cart
4. Complete checkout

### Option C: Buy on Google Domains
1. Go to: https://domains.google.com
2. Search for: `possireports.in`
3. Add to cart
4. Complete checkout

---

## Step 2: Deploy App on Render (If Not Already Done)

1. Go to: https://render.com
2. Sign up with GitHub
3. Create Web Service from your portal repo
4. Deploy (gives you free URL like `my-app.onrender.com`)

---

## Step 3: Add Custom Domain to Render

1. **Go to Render Dashboard**
   - Select your web service (my-web-portal)
   - Click **Settings**

2. **Add Custom Domain**
   - Scroll down to "Custom Domain"
   - Enter: `possireports.in`
   - Click **Add Custom Domain**

3. **Get CNAME Record**
   - Render shows you something like:
   ```
   onrender.com
   ```
   - Copy this value

---

## Step 4: Update DNS Records

### For Namecheap:

1. Log in to: https://www.namecheap.com/dashboard/
2. Click **Domain List**
3. Click **Manage** next to `possireports.in`
4. Go to **Advanced DNS** tab
5. Find "CNAME Record" section
6. Add new record:
   ```
   Host: www
   Type: CNAME
   Value: onrender.com (from Render)
   TTL: 30 min (or default)
   ```
7. Save

**Also add root domain:**
1. Click **Domain** tab
2. Set "Nameservers" to Namecheap defaults (already done usually)
3. Add A record pointing to Render IP (Render will provide)

---

### For GoDaddy:

1. Log in to: https://www.godaddy.com
2. Go to **My Domains**
3. Click **DNS** next to `possireports.in`
4. Add CNAME record:
   ```
   Name: www
   Points to: onrender.com
   TTL: 1 hour
   ```
5. Save

---

## Step 5: Wait for DNS Propagation

DNS changes take **5-30 minutes** to propagate globally.

Check status:
- https://dnschecker.org
- Enter: `possireports.in`
- Wait for all servers to show green

---

## Step 6: Test Your Domain

Once DNS is ready:

1. Visit: `https://possireports.in`
2. Should redirect to your Render app ✅
3. Test login/registration
4. Check HTTPS works (green lock 🔒)

---

## 📋 Complete Checklist

- [ ] Buy domain `possireports.in`
- [ ] Deploy app on Render.com
- [ ] Add custom domain in Render settings
- [ ] Copy CNAME from Render
- [ ] Update DNS records in domain registrar
- [ ] Wait 5-30 minutes for DNS to propagate
- [ ] Test `possireports.in` in browser
- [ ] Verify HTTPS works

---

## ⚡ Your Domain URLs

Once set up, these will work:
- `https://possireports.in` ✅
- `https://www.possireports.in` ✅

---

## 🆘 Troubleshooting

### "Site can't be reached"
- DNS hasn't propagated yet (wait 30 mins)
- Check DNS settings in registrar
- Verify CNAME is correct

### "SSL Certificate Error"
- Wait 10-15 minutes after DNS setup
- Render auto-generates certificate

### "Wrong Page Displayed"
- Clear browser cache (Ctrl+Shift+Delete)
- Try incognito window

---

## 📞 Support Links

- **Namecheap DNS Help**: https://www.namecheap.com/blog/how-to-set-dns-records/
- **Render Custom Domain**: https://render.com/docs/custom-domains
- **DNS Checker**: https://dnschecker.org

---

## 💰 Cost Breakdown

| Item | Cost | Duration |
|------|------|----------|
| possireports.in | $4.88 | 1 year |
| Render hosting | Free | Forever* |
| **TOTAL** | **$4.88** | **Annual** |

*Free tier available; paid tier at $7/month if needed

---

## ✅ Done!

Your portal will be live at **possireports.in** soon! 🚀

**Timeline:**
- Domain purchase: 5 mins
- DNS setup: 5 mins  
- Propagation: 5-30 mins
- **Total: 15-40 mins**

Good luck! Your reports portal is going live! 📊✨
