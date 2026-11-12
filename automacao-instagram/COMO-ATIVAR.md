# Robô do Instagram @oceanosistemas: como ativar

Código: `supabase/functions/instagram-bot/index.ts`, para rodar no projeto Supabase **poggi-precificacao**. As tabelas `ig_bot_events` (registro de cada atendimento) e `ig_bot_config` já estão criadas lá.

## O que o robô faz em TODAS as publicações
- Comentário com palavra-chave (TERRA, PRECO, FICHA, FINANCEIRO, CRM, COMPRAS, PLANO, DIAGNOSTICO e sinônimos) → manda o link certo no direct e responde em público "te mandei no direct".
- Comentário "quero", "link" ou "eu" → lê a legenda do post ("Comente X") e manda o link daquele produto.
- Outros comentários → agradecimento público, com textos variados (dá para desligar com `IG_REPLY_ALL=false`).
- Direct com palavra-chave → manda o link.
- Primeiro direct do dia ou "oi"/"menu" → menu com botões de todos os apps.
- Menção da Oceanos em story → agradece no direct.
- Não responde duas vezes ao mesmo evento e ignora a própria conta (sem loop). Renova o token sozinho a cada 30 dias.

Repostar: a API do Instagram não permite repostar conteúdo de outras pessoas nem publicar stories de terceiros. O robô agradece a menção, e o repost precisa ser feito à mão pelo app.

## Passo a passo no Meta (developers.facebook.com, onde você já está logado)
1. **Criar aplicativo** → caso de uso "Gerenciar mensagens e conteúdo no Instagram" → tipo Empresa.
2. Em **Instagram > Configuração da API com login do Instagram**: adicione a conta @oceanosistemas e clique em **Gerar token**. Guarde o token.
3. Anote a **Chave secreta do app do Instagram**, que aparece nessa mesma tela.
4. Em **Configurar webhooks**:
   - URL de retorno: `https://mdlukjryylxdplcxsloq.supabase.co/functions/v1/instagram-bot`
   - Token de verificação: o valor que você colocar no segredo `IG_VERIFY_TOKEN`
   - Assine os campos: **comments** e **messages**.
5. Permissões: `instagram_business_basic`, `instagram_business_manage_comments`, `instagram_business_manage_messages`.
6. **Atenção:** o Meta só envia webhooks com o app em modo **Ativo (Live)**, e os comentários exigem **Acesso Avançado**. Para isso é preciso enviar o app para **Análise do app** (App Review), com política de privacidade, vídeo mostrando o uso e, possivelmente, verificação da empresa. Essa análise costuma levar alguns dias.

## No Supabase (projeto poggi-precificacao)
1. Edge Functions → criar a função `instagram-bot` com o código de `index.ts`, com **"Verify JWT" desligado** (o Meta não envia login, e a segurança é feita pela assinatura do webhook).
2. Secrets: `IG_VERIFY_TOKEN` (invente uma senha), `IG_APP_SECRET` (passo 3) e `IG_ACCESS_TOKEN` (passo 2).
3. Teste: abra `https://mdlukjryylxdplcxsloq.supabase.co/functions/v1/instagram-bot?status` e confira se aparece `"ok": true`.

## Enquanto o App Review não sai
Use o ManyChat (ele já tem a aprovação do Meta) com as mesmas palavras-chave e textos. Quando o seu app for aprovado, desligue o ManyChat para os dois não responderem juntos.
