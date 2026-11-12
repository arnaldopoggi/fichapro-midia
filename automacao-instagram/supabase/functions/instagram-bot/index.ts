// Robô do Instagram @oceanosistemas — Oceanos Sistemas
// Webhook do "Instagram API with Instagram Login":
//  - comentário com palavra-chave  -> responde em público + manda o link no direct (private reply)
//  - comentário "quero/link/eu"     -> descobre o produto pela legenda do post ("Comente X") e manda o link
//  - outros comentários             -> agradecimento em público (variado)
//  - direct com palavra-chave       -> manda o link
//  - direct sem palavra-chave       -> menu com botões (quick replies)
//  - menção em story                -> agradecimento no direct
// Segredos (Supabase > Edge Functions > Secrets): IG_VERIFY_TOKEN, IG_APP_SECRET, IG_ACCESS_TOKEN
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const GRAPH = "https://graph.instagram.com/v23.0";
const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

type Produto = { nome: string; url: string; oferta: string };
const PRODUTOS: Record<string, Produto> = {
  TERRA: { nome: "Terra à Vista", url: "https://terra.oceanosistemas.com.br", oferta: "o app gratuito para organizar as dívidas e ver a rota até quitar" },
  PRECO: { nome: "Preço Certo", url: "https://precodevenda.oceanosistemas.com.br", oferta: "preço de venda com impostos de hoje e estimativa de 2027. Teste grátis por 7 dias, sem cartão" },
  FICHA: { nome: "Ficha Pro", url: "https://ficha.oceanosistemas.com.br", oferta: "ficha técnica, CMV e preço do prato. Teste grátis por 7 dias, sem cartão" },
  FINANCEIRO: { nome: "Oceanos Financeiro", url: "https://app.oceanosistemas.com.br", oferta: "fluxo de caixa, DRE e conciliação. Teste grátis por 40 dias, sem cartão" },
  CRM: { nome: "CRM Oceanos", url: "https://crm.oceanosistemas.com.br", oferta: "funil de vendas com WhatsApp integrado. Teste grátis por 7 dias" },
  COMPRAS: { nome: "Oceano de Compras", url: "https://compras.oceanosistemas.com.br", oferta: "curva ABC × XYZ e alerta de ruptura. Teste grátis por 7 dias" },
  PLANO: { nome: "Plano de Negócios", url: "https://plano.poggiconsultoria.com.br", oferta: "plano em 8 etapas guiadas com IA e PDF executivo" },
  DIAGNOSTICO: { nome: "Diagnóstico Empresarial", url: "https://coleta.poggiconsultoria.com.br", oferta: "diagnóstico gratuito da sua empresa" },
};
// sinônimos -> chave
const SINONIMOS: Record<string, string> = {
  TERRA: "TERRA", DIVIDA: "TERRA", DIVIDAS: "TERRA",
  PRECO: "PRECO", PRECOCERTO: "PRECO", PRECIFICAR: "PRECO",
  FICHA: "FICHA", FICHAPRO: "FICHA", RESTAURANTE: "FICHA",
  FINANCEIRO: "FINANCEIRO", CAIXA: "FINANCEIRO", DRE: "FINANCEIRO",
  CRM: "CRM", VENDAS: "CRM",
  COMPRAS: "COMPRAS", ESTOQUE: "COMPRAS", ABC: "COMPRAS",
  PLANO: "PLANO",
  DIAGNOSTICO: "DIAGNOSTICO",
};
const PEDIDOS = ["QUERO", "LINK", "EU", "EUQUERO", "MANDA", "INTERESSE", "QUEROO", "QUEROOO"];
const MENU_WORDS = ["MENU", "OI", "OLA", "BOM", "BOA", "INICIO", "AJUDA", "SISTEMAS", "OCEANOS"];

const AGRADECIMENTOS = [
  "Valeu pelo comentário, @{u}! 🙌",
  "Obrigado, @{u}! Se quiser conhecer os apps, manda MENU no direct.",
  "Que bom te ver por aqui, @{u}! 💙",
  "Obrigado pela participação, @{u}!",
  "@{u}, valeu! Qualquer dúvida, chama no direct.",
  "Boa, @{u}! Obrigado por comentar.",
];
const RESP_PUBLICAS = [
  "@{u}, te mandei o link no direct! 📩",
  "Enviado, @{u}! Confere o seu direct. 📩",
  "@{u}, acabei de te mandar no direct. 😉",
  "Pronto, @{u}! O link está no seu direct.",
];
const pick = (a: string[], u: string) => a[Math.floor(Math.random() * a.length)].replaceAll("{u}", u);

function normaliza(t: string) {
  return t.normalize("NFD").replace(/[̀-ͯ]/g, "").toUpperCase();
}
function palavras(t: string) {
  return normaliza(t).split(/[^A-Z0-9]+/).filter(Boolean);
}
function achaProduto(t: string): string | null {
  for (const w of palavras(t)) if (SINONIMOS[w]) return SINONIMOS[w];
  return null;
}
function pedeLink(t: string) {
  return palavras(t).some((w) => PEDIDOS.includes(w));
}

// ---------- token (renova sozinho a cada ~30 dias) ----------
async function token(): Promise<string> {
  const { data } = await db.from("ig_bot_config").select("value, updated_at").eq("key", "access_token").maybeSingle();
  let tk = data?.value || Deno.env.get("IG_ACCESS_TOKEN") || "";
  const idade = data ? (Date.now() - new Date(data.updated_at).getTime()) / 86400000 : 999;
  if (tk && idade > 30) {
    try {
      const r = await fetch(`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${tk}`);
      const j = await r.json();
      if (j.access_token) {
        tk = j.access_token;
        await db.from("ig_bot_config").upsert({ key: "access_token", value: tk, updated_at: new Date().toISOString() });
      } else console.error("refresh falhou", j);
    } catch (e) { console.error("refresh erro", e); }
  }
  return tk;
}

async function graph(path: string, body?: unknown) {
  const tk = await token();
  const r = await fetch(`${GRAPH}${path}${path.includes("?") ? "&" : "?"}access_token=${tk}`, body
    ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
    : undefined);
  const j = await r.json().catch(() => ({}));
  if (!r.ok) console.error("graph erro", path, JSON.stringify(j));
  return j;
}

// ---------- registro + anti-duplicado (o Meta reenvia eventos) ----------
async function primeiraVez(id: string, kind: string, username: string, keyword: string | null, texto: string) {
  const { error } = await db.from("ig_bot_events").insert({ id, kind, username, keyword, texto: texto.slice(0, 500) });
  return !error; // erro = id já existe
}

function textoLink(p: Produto, nomeUsuario?: string) {
  const oi = nomeUsuario ? `Oi, ${nomeUsuario}! ` : "Oi! ";
  return `${oi}Aqui está o link do ${p.nome}, ${p.oferta}:\n\n${p.url}\n\nQualquer dúvida, é só responder aqui. Bons ventos! ⛵`;
}
const QUICK = Object.entries(PRODUTOS).map(([k, p]) => ({ content_type: "text", title: p.nome.slice(0, 20), payload: k }));
const MENU = {
  text: "Oi! Eu sou o assistente da Oceanos Sistemas 🌊\n\nToque no app que você quer conhecer e eu te mando o link. Ou digite a palavra: TERRA, PRECO, FICHA, FINANCEIRO, CRM, COMPRAS, PLANO ou DIAGNOSTICO.",
  quick_replies: QUICK,
};

async function enviaDM(recipientId: string, message: unknown) {
  return graph(`/me/messages`, { recipient: { id: recipientId }, message });
}

// ---------- comentários ----------
async function trataComentario(v: any, contaId: string) {
  const fromId = v?.from?.id, u = v?.from?.username || "", texto = v?.text || "", cid = v?.id;
  if (!cid || !fromId || fromId === contaId) return; // ignora a própria conta
  if (v?.parent_id) return; // ignora respostas dentro de threads
  let chave = achaProduto(texto);
  if (!chave && pedeLink(texto) && v?.media?.id) {
    const m = await graph(`/${v.media.id}?fields=caption`);
    const cap = m?.caption || "";
    const comente = normaliza(cap).match(/COMENTE\s+(?:A\s+PALAVRA\s+)?([A-Z]+)/);
    chave = (comente && SINONIMOS[comente[1]]) || achaProduto(cap);
  }
  if (!(await primeiraVez(`c_${cid}`, "comment", u, chave, texto))) return;
  if (chave) {
    const p = PRODUTOS[chave];
    // private reply: só pode 1 por comentário e até 7 dias depois dele
    await graph(`/me/messages`, { recipient: { comment_id: cid }, message: { text: textoLink(p) } });
    await graph(`/${cid}/replies`, { message: pick(RESP_PUBLICAS, u) });
  } else if (Deno.env.get("IG_REPLY_ALL") !== "false" && palavras(texto).length > 0) {
    await graph(`/${cid}/replies`, { message: pick(AGRADECIMENTOS, u) });
  }
}

// ---------- direct ----------
async function trataMensagem(ev: any, contaId: string) {
  const sender = ev?.sender?.id, msg = ev?.message;
  if (!sender || sender === contaId || !msg || msg.is_echo) return;
  const mid = msg.mid || `${sender}_${ev.timestamp}`;
  const atts = msg.attachments || [];
  if (atts.some((a: any) => a.type === "story_mention")) {
    if (await primeiraVez(`m_${mid}`, "story_mention", sender, null, "")) {
      await enviaDM(sender, { text: "Obrigado por mencionar a Oceanos no seu story! 💙 Se quiser conhecer os apps, digite MENU." });
    }
    return;
  }
  const texto = msg.quick_reply?.payload || msg.text || "";
  const chave = PRODUTOS[texto] ? texto : achaProduto(texto);
  if (!(await primeiraVez(`m_${mid}`, "dm", sender, chave, texto))) return;
  if (chave) return enviaDM(sender, { text: textoLink(PRODUTOS[chave]) });
  const ws = palavras(texto);
  // mostra o menu se pediu, ou se é a primeira conversa nas últimas 24 h
  const pediuMenu = ws.some((w) => MENU_WORDS.includes(w));
  let primeiraConversa = false;
  if (!pediuMenu) {
    const desde = new Date(Date.now() - 86400000).toISOString();
    const { count } = await db.from("ig_bot_events").select("id", { count: "exact", head: true })
      .eq("kind", "dm").eq("username", sender).gte("created_at", desde);
    primeiraConversa = (count ?? 0) <= 1;
  }
  if (pediuMenu || primeiraConversa) return enviaDM(sender, MENU);
  // conversa em andamento sem palavra-chave: não responde (deixa para atendimento humano)
}

// ---------- assinatura ----------
async function assinaturaOk(req: Request, raw: string) {
  const secret = Deno.env.get("IG_APP_SECRET");
  if (!secret) return true;
  const sig = req.headers.get("x-hub-signature-256") || "";
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(raw)));
  const hex = "sha256=" + [...mac].map((b) => b.toString(16).padStart(2, "0")).join("");
  return hex === sig;
}

Deno.serve(async (req) => {
  const url = new URL(req.url);
  if (req.method === "GET") {
    if (url.searchParams.get("hub.mode") === "subscribe" &&
        url.searchParams.get("hub.verify_token") === Deno.env.get("IG_VERIFY_TOKEN")) {
      return new Response(url.searchParams.get("hub.challenge") || "", { status: 200 });
    }
    if (url.searchParams.get("status") !== null) {
      const { count } = await db.from("ig_bot_events").select("id", { count: "exact", head: true });
      return Response.json({ ok: true, eventos: count, token: Boolean(Deno.env.get("IG_ACCESS_TOKEN")), segredo: Boolean(Deno.env.get("IG_APP_SECRET")) });
    }
    return new Response("Forbidden", { status: 403 });
  }
  if (req.method !== "POST") return new Response("ok");
  const raw = await req.text();
  if (!(await assinaturaOk(req, raw))) return new Response("assinatura inválida", { status: 401 });
  let body: any = {};
  try { body = JSON.parse(raw); } catch { return new Response("ok"); }
  const tarefas: Promise<unknown>[] = [];
  for (const entry of body.entry || []) {
    const contaId = String(entry.id || "");
    for (const ch of entry.changes || []) {
      if (ch.field === "comments") tarefas.push(trataComentario(ch.value, contaId));
    }
    for (const ev of entry.messaging || []) tarefas.push(trataMensagem(ev, contaId));
  }
  // responde 200 rápido e termina o trabalho em segundo plano
  // @ts-ignore EdgeRuntime existe no Supabase
  EdgeRuntime.waitUntil(Promise.allSettled(tarefas).then((r) => r.forEach((x) => x.status === "rejected" && console.error(x.reason))));
  return new Response("EVENT_RECEIVED", { status: 200 });
});
