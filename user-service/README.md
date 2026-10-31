# user-service

Cadastro, login e emissão do JWT do Tatame. É o único serviço que tem a **chave privada RSA** e assina tokens; os outros só validam com a chave pública.

**Porta:** 8001 · **Armazenamento:** PostgreSQL (`user_db`) e Redis próprio

## Rotas

| Método | Rota | O que faz |
|---|---|---|
| POST | `/usuarios` | Cadastra um usuário (sempre com o papel `cliente`) |
| POST | `/usuarios/login` | Login com e-mail e senha, devolve o JWT |
| GET | `/auth/github/login` | Redireciona para a autorização no GitHub |
| GET | `/auth/github/callback` | Recebe o retorno do GitHub e devolve o JWT do Tatame |

## Eventos

- **Publica** `usuario.criado` (`usuario_id`, `email`, `telefone`) a cada cadastro, com senha ou pelo GitHub. Se o RabbitMQ estiver fora do ar, o cadastro não falha: o erro vai para o log.

## Detalhes

- **Rate limiting:** cinco tentativas erradas para o mesmo e-mail bloqueiam o login por 15 minutos (`429`). O contador fica no Redis e é zerado num login bem-sucedido.
- **Login com GitHub:** o `state` fica no Redis por 10 minutos e vale uma vez. Só um e-mail primário e verificado é aceito. Uma conta do GitHub não é ligada a uma conta com senha que já exista com o mesmo e-mail (`409`).
- O papel `admin` não pode ser escolhido no cadastro; é atribuído direto no banco.

## Variáveis de ambiente

`DATABASE_URL`, `REDIS_URL`, `RABBITMQ_HOST`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`. As chaves `private_key.pem` e `public_key.pem` são montadas como volume somente leitura, nunca copiadas para a imagem.
