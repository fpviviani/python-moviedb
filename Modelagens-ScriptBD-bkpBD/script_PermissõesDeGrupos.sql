-- Os desenvolvedores terão acesso a somente CRUD na aplicação, não poderão alterar o Schema do banco.
-- É como um usuário de aplicação que tem acesso CRUD a toda a aplicação somente, para poder fazer os 
-- testes necessários no desenvolvimento da aplicação 
CREATE ROLE desenvolvedores;
GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO desenvolvedores;

-- Os usuários comuns são os visitantes da aplicação, e estes tem acesso somente para consultar os filmes 
CREATE ROLE comum;
GRANT SELECT ON TABLE movies TO comum;

-- Os usuários premium são também visitantes da aplicação porém diferentemente dos usuários comuns, 
--estes possuem acesso a consultar não somente aos filmes mais quais estão no top trending, os creditos, etc 
-- Em resumo, podem consultar todo o dado disponibilizado pela aplicação
CREATE ROLE premium;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO premium;

-- Os usuários dba_public são os usuários de banco de dados tendo todo o privilégio no banco da aplicação
CREATE ROLE dba_public;
GRANT ALL PRIVILEGES ON DATABASE "moviedb3" TO dba_public;
GRANT ALL ON ALL TABLES IN SCHEMA public TO dba_public;
GRANT USAGE ON SCHEMA public TO dba_public;

-- Os usuários de aplicação são os que irão gerenciar aplicação, ou seja será o que irão popular o banco, remover, alterar ou consultar
-- os dados, os catálogos de filmes, etc. São os geradores de conteúdo. Em outras palavra são os funcionários da empresa que adquiriu o sistema.
-- Eles possuem o mesmo acesso do desenvolvedor pois para o desenvolvedor construir a aplicação terá que assumir o papel desse usuário para
-- poder realizar os testes necessários enquanto constroem a aplicação.
CREATE ROLE aplicacao;
GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aplicacao;