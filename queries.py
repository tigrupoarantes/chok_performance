def query_vendas(filtro_perfil=None, data_inicio=None, data_fim=None):
    sql = """
    SELECT
        ped_vda.nu_ped,
        ped_vda.dt_ped,
        vendedor.cd_vend,
        vendedor.nome_gue AS vendedor,
        cliente.nome AS cliente,
        SUM(it_pedv.vl_venda) AS vl_venda
    FROM MOINHO.dbo.ped_vda ped_vda
    INNER JOIN MOINHO.dbo.it_pedv it_pedv
        ON it_pedv.nu_ped = ped_vda.nu_ped
    INNER JOIN MOINHO.dbo.vendedor vendedor
        ON vendedor.cd_vend = ped_vda.cd_vend
    INNER JOIN MOINHO.dbo.cliente cliente
        ON cliente.cd_clien = ped_vda.cd_clien
    WHERE ped_vda.situacao NOT IN ('CA','RB','DV')
    """

    # 📅 Filtro de período
    if data_inicio and data_fim:
        sql += f"""
        AND ped_vda.dt_ped BETWEEN '{data_inicio}' AND '{data_fim}'
        """

    # 👤 Filtro por perfil
    if filtro_perfil:
        sql += f" AND {filtro_perfil}"

    sql += """
    GROUP BY
        ped_vda.nu_ped,
        ped_vda.dt_ped,
        vendedor.cd_vend,
        vendedor.nome_gue,
        cliente.nome
    ORDER BY ped_vda.dt_ped DESC
    """

    return sql