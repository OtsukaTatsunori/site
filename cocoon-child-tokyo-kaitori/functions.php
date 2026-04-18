<?php //子テーマ用関数
if ( ! defined( 'ABSPATH' ) ) exit;

// =====================================================
// 子テーマ用のカスタム関数をここに書く
//
// 注意: Cocoon は親テーマのスタイルを自動で読み込むため
// wp_enqueue_style() の記述は不要です。
// （書くとCSSが二重読み込みされ、デザインが崩れます）
// =====================================================


// -----------------------------------------------------
// カスタム投稿タイプ: 業者情報（company）
// エリア別・サービス別に業者を整理するための CPT
// -----------------------------------------------------
add_action( 'init', 'tk_register_company_post_type' );
function tk_register_company_post_type() {
	$labels = array(
		'name'               => '業者情報',
		'singular_name'      => '業者',
		'menu_name'          => '業者情報',
		'add_new'            => '新規業者を追加',
		'add_new_item'       => '新しい業者を追加',
		'edit_item'          => '業者を編集',
		'new_item'           => '新しい業者',
		'view_item'          => '業者を表示',
		'search_items'       => '業者を検索',
		'not_found'          => '業者が見つかりません',
		'not_found_in_trash' => 'ゴミ箱に業者はありません',
	);

	register_post_type( 'company', array(
		'labels'              => $labels,
		'public'              => true,
		'has_archive'         => true,
		'rewrite'             => array( 'slug' => 'company' ),
		'menu_icon'           => 'dashicons-store',
		'menu_position'       => 5,
		'supports'            => array( 'title', 'editor', 'thumbnail', 'excerpt' ),
		'show_in_rest'        => true, // ブロックエディタ対応
	) );
}

// -----------------------------------------------------
// タクソノミー: 対応エリア（company_area）
// -----------------------------------------------------
add_action( 'init', 'tk_register_company_area_taxonomy' );
function tk_register_company_area_taxonomy() {
	register_taxonomy( 'company_area', 'company', array(
		'labels' => array(
			'name'          => '対応エリア',
			'singular_name' => '対応エリア',
			'menu_name'     => '対応エリア',
		),
		'hierarchical' => true,
		'public'       => true,
		'rewrite'      => array( 'slug' => 'company-area' ),
		'show_in_rest' => true,
	) );
}

// -----------------------------------------------------
// タクソノミー: 対応サービス（company_service）
// -----------------------------------------------------
add_action( 'init', 'tk_register_company_service_taxonomy' );
function tk_register_company_service_taxonomy() {
	register_taxonomy( 'company_service', 'company', array(
		'labels' => array(
			'name'          => '対応サービス',
			'singular_name' => '対応サービス',
			'menu_name'     => '対応サービス',
		),
		'hierarchical' => true,
		'public'       => true,
		'rewrite'      => array( 'slug' => 'company-service' ),
		'show_in_rest' => true,
	) );
}

// -----------------------------------------------------
// 業者情報のメタボックス（カスタムフィールド）
// 料金目安・電話番号・公式URL（アフィリエイト）・特徴
// -----------------------------------------------------
add_action( 'add_meta_boxes', 'tk_add_company_meta_boxes' );
function tk_add_company_meta_boxes() {
	add_meta_box(
		'tk_company_details',
		'業者詳細情報',
		'tk_render_company_meta_box',
		'company',
		'normal',
		'high'
	);
}

function tk_render_company_meta_box( $post ) {
	wp_nonce_field( 'tk_company_meta_save', 'tk_company_meta_nonce' );

	$price_range       = get_post_meta( $post->ID, '_tk_price_range', true );
	$business_hours    = get_post_meta( $post->ID, '_tk_business_hours', true );
	$phone             = get_post_meta( $post->ID, '_tk_phone', true );
	$official_url      = get_post_meta( $post->ID, '_tk_official_url', true );
	$affiliate_url_key = get_post_meta( $post->ID, '_tk_affiliate_url_key', true );
	$features          = get_post_meta( $post->ID, '_tk_features', true );
	?>
	<style>
		.tk-meta-table { width: 100%; }
		.tk-meta-table th { text-align: left; width: 180px; padding: 8px 4px; vertical-align: top; }
		.tk-meta-table td { padding: 8px 4px; }
		.tk-meta-table input[type="text"],
		.tk-meta-table textarea { width: 100%; }
	</style>
	<table class="tk-meta-table">
		<tr>
			<th><label for="tk_price_range">料金目安</label></th>
			<td><input type="text" id="tk_price_range" name="tk_price_range" value="<?php echo esc_attr( $price_range ); ?>" placeholder="例: 1K 30,000円〜" /></td>
		</tr>
		<tr>
			<th><label for="tk_business_hours">営業時間</label></th>
			<td><input type="text" id="tk_business_hours" name="tk_business_hours" value="<?php echo esc_attr( $business_hours ); ?>" placeholder="例: 9:00〜20:00 年中無休" /></td>
		</tr>
		<tr>
			<th><label for="tk_phone">電話番号</label></th>
			<td><input type="text" id="tk_phone" name="tk_phone" value="<?php echo esc_attr( $phone ); ?>" placeholder="例: 0120-XXX-XXX" /></td>
		</tr>
		<tr>
			<th><label for="tk_official_url">公式サイトURL</label></th>
			<td><input type="text" id="tk_official_url" name="tk_official_url" value="<?php echo esc_attr( $official_url ); ?>" placeholder="例: https://example.com/" /></td>
		</tr>
		<tr>
			<th><label for="tk_affiliate_url_key">アフィリエイトURLキー</label></th>
			<td>
				<input type="text" id="tk_affiliate_url_key" name="tk_affiliate_url_key" value="<?php echo esc_attr( $affiliate_url_key ); ?>" placeholder="例: company-a" />
				<p class="description">ASPリンクのプレースホルダキー。ショートコード <code>[tk_affiliate_link key="..."]</code> で呼び出す。</p>
			</td>
		</tr>
		<tr>
			<th><label for="tk_features">特徴（3点程度、改行区切り）</label></th>
			<td><textarea id="tk_features" name="tk_features" rows="4" placeholder="例:&#10;即日対応&#10;女性スタッフ在籍&#10;遺品供養対応"><?php echo esc_textarea( $features ); ?></textarea></td>
		</tr>
	</table>
	<?php
}

add_action( 'save_post_company', 'tk_save_company_meta' );
function tk_save_company_meta( $post_id ) {
	if ( ! isset( $_POST['tk_company_meta_nonce'] ) ) return;
	if ( ! wp_verify_nonce( $_POST['tk_company_meta_nonce'], 'tk_company_meta_save' ) ) return;
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;
	if ( ! current_user_can( 'edit_post', $post_id ) ) return;

	$fields = array(
		'_tk_price_range'       => 'tk_price_range',
		'_tk_business_hours'    => 'tk_business_hours',
		'_tk_phone'             => 'tk_phone',
		'_tk_official_url'      => 'tk_official_url',
		'_tk_affiliate_url_key' => 'tk_affiliate_url_key',
		'_tk_features'          => 'tk_features',
	);

	foreach ( $fields as $meta_key => $post_key ) {
		if ( isset( $_POST[ $post_key ] ) ) {
			$value = wp_unslash( $_POST[ $post_key ] );
			if ( $post_key === 'tk_features' ) {
				update_post_meta( $post_id, $meta_key, sanitize_textarea_field( $value ) );
			} elseif ( $post_key === 'tk_official_url' ) {
				update_post_meta( $post_id, $meta_key, esc_url_raw( $value ) );
			} else {
				update_post_meta( $post_id, $meta_key, sanitize_text_field( $value ) );
			}
		}
	}
}

// -----------------------------------------------------
// アフィリエイトリンク プレースホルダ用ショートコード
// 使い方: [tk_affiliate_link key="company-a" label="公式サイトを見る"]
// ASP確定前は official_url に、確定後は差し替えた URL にリンク
// -----------------------------------------------------
add_shortcode( 'tk_affiliate_link', 'tk_affiliate_link_shortcode' );
function tk_affiliate_link_shortcode( $atts ) {
	$atts = shortcode_atts( array(
		'key'   => '',
		'label' => '▶ 公式サイトを見る',
		'class' => 'btn btn-primary',
	), $atts, 'tk_affiliate_link' );

	$url = tk_resolve_affiliate_url( $atts['key'] );
	if ( empty( $url ) ) return '';

	return sprintf(
		'<a href="%s" rel="nofollow sponsored" class="%s" target="_blank">%s</a>',
		esc_url( $url ),
		esc_attr( $atts['class'] ),
		esc_html( $atts['label'] )
	);
}

// アフィリエイトキーから URL を解決する
// 1. option 'tk_affiliate_urls' （key => url の連想配列）を最優先
// 2. なければ、該当キーを持つ company CPT の official_url にフォールバック
function tk_resolve_affiliate_url( $key ) {
	if ( empty( $key ) ) return '';

	$map = get_option( 'tk_affiliate_urls', array() );
	if ( is_array( $map ) && ! empty( $map[ $key ] ) ) {
		return $map[ $key ];
	}

	$query = new WP_Query( array(
		'post_type'      => 'company',
		'posts_per_page' => 1,
		'meta_key'       => '_tk_affiliate_url_key',
		'meta_value'     => $key,
		'fields'         => 'ids',
		'no_found_rows'  => true,
	) );

	if ( $query->have_posts() ) {
		$company_id = $query->posts[0];
		return get_post_meta( $company_id, '_tk_official_url', true );
	}

	return '';
}
