from clusters.default_cluster import DefaultCluster

# default_1U_cluster: true 前提
class TrackballMB(DefaultCluster):
    translation_offset = [-44, -19, -7]
    rotation_offset = [19, -19, -5]
    thumb_plate_tl_rotation = 5

    @staticmethod
    def name():
        return "TRACKBALL_MB"

    def __init__(self, parent_locals):
        self.num_keys = 4
        self.is_tb = True
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    # トラックボールの位置と回転
    def position_rotation(self):
        rot = self.rotation_offset
        pos = self.thumborigin()
        for i in range(len(pos)):
            pos[i] = pos[i] + self.translation_offset[i]
        return pos, rot

    def track_place(self, shape):
        pos, rot = self.position_rotation()
        shape = rotate(shape, rot)
        shape = translate(shape, pos)
        return shape

    # このキーだけすこし移動
    def mr_place(self, shape):
        debugprint('mr_place()')
        shape = super().mr_place(shape)
        shape = rotate(shape, [0, 0, 0])
        shape = translate(shape, [7, -4, 0])
        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
            self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
            self.br_place(rotate(shape, [0, 0, self.thumb_plate_br_rotation])),
        ])

    def tb_post_r(self):
        debugprint('post_r()')
        radius = ball_diameter/2 + ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_tr(self):
        debugprint('post_tr()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )

    def tb_post_t(self):
        debugprint('post_t()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.0*(radius - post_adj), 1.0*(radius - post_adj), 0]
                         )

    def tb_post_tl(self):
        debugprint('post_tl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), 0.866*(radius - post_adj), 0]
                         )

    def tb_post_l(self):
        debugprint('post_l()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-1.0*(radius - post_adj), 0.0*(radius - post_adj), 0]
                         )

    def tb_post_bl(self):
        debugprint('post_bl()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [-0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )

    def tb_post_b(self):
        debugprint('post_b()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.0*(radius - post_adj), -1.0*(radius - post_adj), 0]
                         )

    def tb_post_br(self):
        debugprint('post_br()')
        radius = ball_diameter/2+ball_wall_thickness + ball_gap
        return translate(web_post(),
                         [0.5*(radius - post_adj), -0.866*(radius - post_adj), 0]
                         )

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(single_plate(side=side))
        return shape

    # 親指クラスタ内要素間隙間を埋める
    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        # top right and middle right
        hulls.append(
            triangle_hulls(
                [
                    self.tr_place(web_post_bl()),
                    self.tr_place(web_post_br()),
                    self.mr_place(web_post_br()),
                    self.mr_place(web_post_tr()),
                    self.tr_place(web_post_bl()),
                ]
            )
        )

        # bottom two on the right
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.mr_place(web_post_bl()),
                ]
            )
        )

        # bottom two on the left
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.mr_place(web_post_bl()),
                ]
            )
        )

        # centers of the bottom four
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.bl_place(web_post_br()),
                    self.ml_place(web_post_tl()),
                    self.ml_place(web_post_bl()),
                ]
            )
        )

        # top two to the middle two, starting on the left
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tl()),
                    self.bl_place(web_post_bl()),
                    self.br_place(web_post_tr()),
                    self.bl_place(web_post_br()),
                ]
            )
        )

        # trackball and others
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.track_place(self.tb_post_l()),
                    self.ml_place(web_post_tl()),
                    self.track_place(self.tb_post_l()),
                    self.ml_place(web_post_bl()),
                    self.track_place(self.tb_post_bl()),
                    self.bl_place(web_post_tr()),
                    self.track_place(self.tb_post_bl()),
                    self.bl_place(web_post_br()),
                    self.track_place(self.tb_post_b()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_b()),
                    self.mr_place(web_post_tl()),
                    self.track_place(self.tb_post_br()),
                    self.mr_place(web_post_tr()),
                    self.track_place(self.tb_post_r()),
                    self.tr_place(web_post_bl()),
                    self.track_place(self.tb_post_r()),
                    self.tr_place(web_post_tl()),
                    self.track_place(self.tb_post_tr()),
                ]
            )
        )

        # 親指クラスタ右上と本体左下の接続
        hulls.append(
            triangle_hulls(
                [
                    self.track_place(self.tb_post_t()),
                    cluster_key_place(web_post_bl(), 0, cornerrow),
                    self.track_place(self.tb_post_tr()),
                    cluster_key_place(web_post_bl(), 1, cornerrow),
                    self.tr_place(web_post_tl()),
                    cluster_key_place(web_post_bl(), 1, cornerrow),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(web_post_br(), 1, cornerrow),
                    cluster_key_place(web_post_bl(), 2, cornerrow),
                    cluster_key_place(web_post_tl(), 2, lastrow),
                    self.tr_place(web_post_tr()),
                    cluster_key_place(web_post_bl(), 2, lastrow),
                    self.tr_place(web_post_br()),
                    cluster_key_place(web_post_br(), 2, lastrow),
                    self.tr_place(web_post_br()),
                    cluster_key_place(web_post_bl(), 3, lastrow),
                    self.tr_place(web_post_br()),
                ]
            )
        )

        if not full_last_rows:
            hulls.append(
                triangle_hulls(
                    [
                        cluster_key_place(web_post_tr(), 3, lastrow),
                        cluster_key_place(web_post_br(), 3, lastrow),
                        cluster_key_place(web_post_tr(), 3, lastrow),
                        cluster_key_place(web_post_bl(), 4, cornerrow),
                    ]
                )
            )

        return union(hulls)

    # 親指クラスタの壁面
    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = union([wall_brace(self.mr_place, 0, -1, web_post_br(), self.tr_place, 0, -1, web_post_br())])
        shape = union([shape, wall_brace(self.mr_place, 0, -1, web_post_br(), self.mr_place, 0, -1, web_post_bl())])
        shape = union([shape, wall_brace(self.br_place, 0, -1, web_post_br(), self.br_place, 0, -1, web_post_bl())])
        shape = union([shape, wall_brace(self.ml_place, -0.3, 1, web_post_tr(), self.ml_place, 0, 1, web_post_tl())])
        shape = union([shape, wall_brace(self.bl_place, 0, 1, web_post_tr(), self.bl_place, 0, 1, web_post_tl())])
        shape = union([shape, wall_brace(self.br_place, -1, 0, web_post_tl(), self.br_place, -1, 0, web_post_bl())])
        shape = union([shape, wall_brace(self.bl_place, -1, 0, web_post_tl(), self.bl_place, -1, 0, web_post_bl())])
        # thumb, corners
        shape = union([shape, wall_brace(self.br_place, -1, 0, web_post_bl(), self.br_place, 0, -1, web_post_bl())])
        shape = union([shape, wall_brace(self.bl_place, -1, 0, web_post_tl(), self.bl_place, 0, 1, web_post_tl())])
        # thumb, tweeners
        shape = union([shape, wall_brace(self.mr_place, 0, -1, web_post_bl(), self.br_place, 0, -1, web_post_br())])
        shape = union([shape, wall_brace(self.ml_place, 0, 1, web_post_tl(), self.bl_place, 0, 1, web_post_tr())])
        shape = union([shape, wall_brace(self.bl_place, -1, 0, web_post_bl(), self.br_place, -1, 0, web_post_tl())])
        shape = union([shape,
                       wall_brace(self.tr_place, 0, -1, web_post_br(), (lambda sh: cluster_key_place(sh, 3, lastrow)), 0,
                                  -1, web_post_bl())])
        return shape

    # 親指クラスタと本体を接続する部分
    def connection(self, side='right'):
        print('connection()')

        shape = union([])

        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        shape = union([bottom_hull(
            [
                left_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                self.ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
                self.ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
            ]
        )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1,
                                              low_corner=True, side=side),
                               self.ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
                               self.ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )
                       ])

        shape = union([shape, hull_from_shapes(
            [
                left_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_key_place(translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                left_key_place(translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        shape = union([shape, hull_from_shapes(
            [
                left_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
                left_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True, side=side),
                cluster_key_place(web_post_bl(), 0, cornerrow),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        shape = union([shape, hull_from_shapes(
            [
                self.ml_place(web_post_tr()),
                self.ml_place(translate(web_post_tr(), wall_locate1(-0.3, 1))),
                self.ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
                self.ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
                self.tl_place(self.thumb_post_tl()),
            ]
        )])

        return shape
