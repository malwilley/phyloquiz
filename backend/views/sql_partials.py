select_node = """
    SELECT n.id, n.ott, popularity, age, name, v.vernacular, q.num_quiz_leaves, i1.src, i1.src_id, i2.src, i2.src_id,  i3.src, i3.src_id,  i4.src, i4.src_id,  i5.src, i5.src_id,  i6.src, i6.src_id,  i7.src, i7.src_id,  i8.src, i8.src_id
    FROM ordered_nodes n
    JOIN quiz_nodes q on q.node_id = n.id
    JOIN vernacular_by_ott v ON v.ott = n.ott and v.lang_primary = 'en' and v.preferred
    JOIN images_by_ott i1 ON i1.overall_best_any AND i1.ott = n.rep1
    JOIN images_by_ott i2 ON i2.overall_best_any AND i2.ott = n.rep2
    JOIN images_by_ott i3 ON i3.overall_best_any AND i3.ott = n.rep3
    JOIN images_by_ott i4 ON i4.overall_best_any AND i4.ott = n.rep4
    JOIN images_by_ott i5 ON i5.overall_best_any AND i5.ott = n.rep5
    JOIN images_by_ott i6 ON i6.overall_best_any AND i6.ott = n.rep6
    JOIN images_by_ott i7 ON i7.overall_best_any AND i7.ott = n.rep7
    JOIN images_by_ott i8 ON i8.overall_best_any AND i8.ott = n.rep8
    """
